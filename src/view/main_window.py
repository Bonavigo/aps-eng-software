"""Janela principal da aplicação."""

from __future__ import annotations

import queue
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.view.about_window import AboutWindow
from src.view.results_window import ResultsWindow
from src.view.tutorial_window import TutorialWindow


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    """Janela principal simples e funcional."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.title("SCALE - Emergy APS")
        self.geometry("900x600")
        self.workspace_var = ctk.StringVar()
        self.graph_var = ctk.StringVar()
        self.uev_var = ctk.StringVar()
        self.threshold_var = ctk.StringVar(value="0.1")
        self._fila_progresso: queue.Queue[float] = queue.Queue()
        self._fila_resultados: queue.Queue[dict] = queue.Queue()
        self._resultado_atual: dict | None = None
        self._itens_workspace: list[ctk.CTkLabel] = []
        self._item_workspace_selecionado: ctk.CTkLabel | None = None
        self._build()
        self.after(100, self._processar_filas)

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        barra = ctk.CTkFrame(self)
        barra.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        barra.grid_columnconfigure(3, weight=1)
        ctk.CTkButton(barra, text="Início", command=lambda: self._log("Início selecionado.")).grid(
            row=0, column=0, padx=(0, 8), pady=8
        )
        ctk.CTkButton(barra, text="Tutorial", command=lambda: TutorialWindow(self)).grid(
            row=0, column=1, padx=(0, 8), pady=8
        )
        ctk.CTkButton(barra, text="Sobre", command=lambda: AboutWindow(self)).grid(
            row=0, column=2, padx=(0, 8), pady=8
        )

        top = ctk.CTkFrame(self)
        top.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        top.grid_columnconfigure(0, weight=1)
        ctk.CTkEntry(top, textvariable=self.workspace_var).grid(row=0, column=0, sticky="ew", padx=(8, 4), pady=8)
        ctk.CTkButton(top, text="Navegar", command=self._selecionar_workspace).grid(
            row=0, column=1, padx=(4, 8), pady=8
        )

        body = ctk.CTkFrame(self)
        body.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        body.grid_columnconfigure(0, weight=0, minsize=260)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(8, 6), pady=8)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(left, text="Espaço de Trabalho:", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=8, pady=(8, 4)
        )
        self.lista = ctk.CTkScrollableFrame(left)
        self.lista.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        right = ctk.CTkFrame(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 8), pady=8)
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.tabs = ctk.CTkTabview(right)
        self.tabs.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.tabs.add("Cálculo Completo")
        aba = self.tabs.tab("Cálculo Completo")
        aba.grid_columnconfigure(1, weight=1)

        for linha_idx, (texto, var) in enumerate(
            [
                ("Arquivo de Rede (CSV)", self.graph_var),
                ("Arquivo de UEVs (JSON)", self.uev_var),
                ("Limiar de Propagação", self.threshold_var),
            ]
        ):
            linha = ctk.CTkFrame(aba)
            linha.grid(row=linha_idx, column=0, sticky="ew", padx=8, pady=4)
            linha.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(linha, text=texto, width=180, anchor="w").grid(row=0, column=0, padx=(8, 6), pady=8)
            ctk.CTkEntry(linha, textvariable=var).grid(row=0, column=1, sticky="ew", padx=(0, 6), pady=8)
            if texto != "Limiar de Propagação":
                ctk.CTkButton(linha, text="Navegar", command=lambda v=var: self._buscar_arquivo(v)).grid(
                    row=0, column=2, padx=(0, 8), pady=8
                )

        ctk.CTkButton(aba, text="Iniciar Cálculo", command=self._calcular).grid(
            row=3, column=0, pady=(12, 8), padx=8, sticky="ew"
        )
        self.progresso = ctk.CTkProgressBar(aba)
        self.progresso.grid(row=4, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.progresso.set(0)

        botoes = ctk.CTkFrame(aba)
        botoes.grid(row=5, column=0, sticky="ew", padx=8, pady=(0, 8))
        for coluna in range(3):
            botoes.grid_columnconfigure(coluna, weight=1)
        self.btn_csv = ctk.CTkButton(botoes, text="Exportar CSV", state="disabled", command=lambda: self._exportar("csv"))
        self.btn_pdf = ctk.CTkButton(botoes, text="Exportar PDF", state="disabled", command=lambda: self._exportar("pdf"))
        self.btn_png = ctk.CTkButton(
            botoes, text="Exportar Grafo (PNG)", state="disabled", command=lambda: self._exportar("png")
        )
        self.btn_csv.grid(row=0, column=0, padx=4, pady=8, sticky="ew")
        self.btn_pdf.grid(row=0, column=1, padx=4, pady=8, sticky="ew")
        self.btn_png.grid(row=0, column=2, padx=4, pady=8, sticky="ew")

        self.log = ctk.CTkTextbox(aba, height=160, wrap="word")
        self.log.grid(row=6, column=0, sticky="nsew", padx=8, pady=(0, 8))
        aba.grid_rowconfigure(6, weight=1)
        self.log.configure(state="disabled")

    def _selecionar_workspace(self) -> None:
        caminho = filedialog.askdirectory()
        if caminho:
            self.workspace_var.set(caminho)
            self._popular_lista_workspace(caminho)
            self._log(f"Workspace carregado: {caminho}")

    def _popular_lista_workspace(self, caminho: str) -> None:
        for widget in self._itens_workspace:
            widget.destroy()
        self._itens_workspace.clear()
        self._item_workspace_selecionado = None

        for item in sorted(p.name for p in Path(caminho).iterdir() if p.is_file()):
            label = ctk.CTkLabel(self.lista, text=item, anchor="w", justify="left", corner_radius=6)
            label._arquivo_nome = item  # type: ignore[attr-defined]
            label.bind("<Button-1>", self._carregar_selecionado)
            label.pack(fill="x", padx=4, pady=3)
            self._itens_workspace.append(label)

        if not self._itens_workspace:
            vazio = ctk.CTkLabel(self.lista, text="Nenhum arquivo encontrado.", anchor="w", justify="left")
            vazio.pack(fill="x", padx=4, pady=3)
            self._itens_workspace.append(vazio)

    def _marcar_item_workspace(self, widget: ctk.CTkLabel | None) -> None:
        if self._item_workspace_selecionado and self._item_workspace_selecionado is not widget:
            self._item_workspace_selecionado.configure(fg_color="transparent")
        self._item_workspace_selecionado = widget
        if widget:
            widget.configure(fg_color=("gray70", "gray25"))

    def _carregar_selecionado(self, event=None) -> None:
        widget = getattr(event, "widget", None)
        arquivo = getattr(widget, "_arquivo_nome", None)
        if not arquivo:
            return
        caminho = Path(self.workspace_var.get()) / arquivo
        self._marcar_item_workspace(widget)
        if caminho.suffix.lower() == ".csv":
            self.graph_var.set(str(caminho))
            self._log(f"Arquivo de rede selecionado: {caminho.name}")
        elif caminho.suffix.lower() == ".json":
            self.uev_var.set(str(caminho))
            self._log(f"Arquivo de UEVs selecionado: {caminho.name}")

    def _buscar_arquivo(self, var: ctk.StringVar) -> None:
        caminho = filedialog.askopenfilename(
            initialdir=self.workspace_var.get() or None,
            filetypes=[("Arquivos CSV", "*.csv"), ("Arquivos JSON", "*.json"), ("Arquivos suportados", "*.csv *.json")],
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
        self.progresso.set(0)
        self.controller.iniciar_calculo(params, on_done=lambda resultados: self._fila_resultados.put(resultados))

    def _processar_filas(self) -> None:
        while not self._fila_progresso.empty():
            progresso = float(self._fila_progresso.get())
            self.progresso.set(progresso / 100.0 if progresso > 1 else progresso)
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
        self.log.configure(state="normal")
        self.log.insert("end", f"{mensagem}\n")
        self.log.see("end")
        self.log.configure(state="disabled")
