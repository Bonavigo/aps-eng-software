"""Janela principal da aplicação."""

from __future__ import annotations

import queue
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from src.view.about_window import AboutWindow
from src.view.results_window import ResultsWindow
from src.view.tutorial_window import TutorialWindow


class MainWindow(tk.Tk):
    """Janela principal simples e funcional."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.title("SCALE - Emergy APS")
        self.geometry("900x600")
        self.workspace_var = tk.StringVar()
        self.graph_var = tk.StringVar()
        self.uev_var = tk.StringVar()
        self.threshold_var = tk.StringVar(value="0.1")
        self._fila_progresso: queue.Queue[float] = queue.Queue()
        self._fila_resultados: queue.Queue[dict] = queue.Queue()
        self._resultado_atual: dict | None = None
        self._build()
        self.after(100, self._processar_filas)

    def _build(self) -> None:
        barra = tk.Frame(self)
        barra.pack(fill="x")
        tk.Button(barra, text="Home", command=lambda: self._log("Home selecionado.")).pack(side="left")
        tk.Button(barra, text="Tutorial", command=lambda: TutorialWindow(self)).pack(side="left")
        tk.Button(barra, text="About", command=lambda: AboutWindow(self)).pack(side="left")

        top = tk.Frame(self)
        top.pack(fill="x", padx=8, pady=8)
        tk.Entry(top, textvariable=self.workspace_var, width=70).pack(side="left", fill="x", expand=True)
        tk.Button(top, text="Browse", command=self._selecionar_workspace).pack(side="left")

        body = tk.PanedWindow(self, orient="horizontal")
        body.pack(fill="both", expand=True, padx=8, pady=8)
        left = tk.Frame(body, width=200)
        tk.Label(left, text="Workspace :", anchor="w").pack(fill="x")
        self.lista = tk.Listbox(left)
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", self._carregar_selecionado)
        body.add(left)

        right = ttk.Notebook(body)
        body.add(right)
        aba = tk.Frame(right)
        right.add(aba, text="Complete Calculation")
        for texto, var in [("Graph File", self.graph_var), ("Input File", self.uev_var), ("Threshold", self.threshold_var)]:
            linha = tk.Frame(aba)
            linha.pack(fill="x", pady=4)
            tk.Label(linha, text=texto, width=14, anchor="w").pack(side="left")
            tk.Entry(linha, textvariable=var).pack(side="left", fill="x", expand=True)
            if texto != "Threshold":
                tk.Button(linha, text="...", width=4, command=lambda v=var: self._buscar_arquivo(v)).pack(side="left", padx=4)
        tk.Button(aba, text="Start Calculation", command=self._calcular).pack(pady=8)
        self.progresso = ttk.Progressbar(aba, maximum=100)
        self.progresso.pack(fill="x", pady=4)
        botoes = tk.Frame(aba)
        botoes.pack(fill="x", pady=4)
        self.btn_csv = tk.Button(botoes, text="Export CSV", state="disabled", command=lambda: self._exportar("csv"))
        self.btn_pdf = tk.Button(botoes, text="Export PDF", state="disabled", command=lambda: self._exportar("pdf"))
        self.btn_png = tk.Button(botoes, text="Export Grafo PNG", state="disabled", command=lambda: self._exportar("png"))
        self.btn_csv.pack(side="left", padx=4)
        self.btn_pdf.pack(side="left", padx=4)
        self.btn_png.pack(side="left", padx=4)
        self.log = tk.Text(aba, height=10)
        self.log.pack(fill="both", expand=True)

    def _selecionar_workspace(self) -> None:
        caminho = filedialog.askdirectory()
        if caminho:
            self.workspace_var.set(caminho)
            self.lista.delete(0, "end")
            for item in sorted(p.name for p in Path(caminho).iterdir() if p.is_file()):
                self.lista.insert("end", item)
            self._log(f"Workspace carregado: {caminho}")

    def _carregar_selecionado(self, _event=None) -> None:
        if not self.lista.curselection():
            return
        arquivo = self.lista.get(self.lista.curselection()[0])
        caminho = Path(self.workspace_var.get()) / arquivo
        if caminho.suffix.lower() == ".csv":
            self.graph_var.set(str(caminho))
            self._log(f"Arquivo de grafo selecionado: {caminho.name}")
        elif caminho.suffix.lower() == ".json":
            self.uev_var.set(str(caminho))
            self._log(f"Arquivo de UEV selecionado: {caminho.name}")

    def _buscar_arquivo(self, var: tk.StringVar) -> None:
        caminho = filedialog.askopenfilename(
            initialdir=self.workspace_var.get() or None,
            filetypes=[("Arquivos suportados", "*.csv *.json"), ("CSV", "*.csv"), ("JSON", "*.json")],
        )
        if caminho:
            var.set(caminho)
            self._log(f"Arquivo selecionado: {Path(caminho).name}")

    def _calcular(self) -> None:
        params = {
            "caminho_grafo": self.graph_var.get(),
            "caminho_uevs": self.uev_var.get(),
            "threshold": self.threshold_var.get() or "0.1",
            "callback": lambda progresso: self._fila_progresso.put(progresso),
        }
        self._log("Iniciando cálculo...")
        self.progresso.configure(value=0)
        self.controller.iniciar_calculo(params, on_done=lambda resultados: self._fila_resultados.put(resultados))

    def _processar_filas(self) -> None:
        while not self._fila_progresso.empty():
            self.progresso.configure(value=self._fila_progresso.get() * 100)
        while not self._fila_resultados.empty():
            self._resultado_atual = self._fila_resultados.get()
            ResultsWindow(self, resultados=self._resultado_atual)
            self.btn_csv.configure(state="normal")
            self.btn_pdf.configure(state="normal")
            self.btn_png.configure(state="normal")
            self._log("Cálculo concluído.")
        self.after(100, self._processar_filas)

    def _exportar(self, tipo: str) -> None:
        if not self._resultado_atual:
            self._log("Não há resultados para exportar.")
            return
        if tipo == "csv":
            filtro = [("CSV", "*.csv")]
            extensao = ".csv"
        elif tipo == "pdf":
            filtro = [("PDF", "*.pdf")]
            extensao = ".pdf"
        else:
            filtro = [("PNG", "*.png")]
            extensao = ".png"
        caminho = filedialog.asksaveasfilename(defaultextension=extensao, filetypes=filtro)
        if caminho:
            self.controller.ultimos_resultados = self._resultado_atual
            self.controller.exportar_resultados(tipo, caminho)
            self._log(f"Exportado: {caminho}")

    def _log(self, mensagem: str) -> None:
        self.log.insert("end", f"{mensagem}\n")
        self.log.see("end")
