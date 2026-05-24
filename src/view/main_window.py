"""Janela principal da aplicação."""

from __future__ import annotations

import queue
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from src.view.about_window import AboutWindow
from src.view.dialogs import mostrar_erro
from src.view.results_window import ResultsWindow
from src.view.tutorial_window import TutorialWindow


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    """Janela principal da aplicação EmerCalc."""

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self._largura_janela = 900
        self._altura_janela = 600
        self.title("EmerCalc")
        self.geometry(f"{self._largura_janela}x{self._altura_janela}")
        self.minsize(self._largura_janela, self._altura_janela)
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self.workspace_var = ctk.StringVar()
        self.graph_var = ctk.StringVar()
        self.uev_var = ctk.StringVar()
        self.threshold_var = ctk.StringVar(value="0.1")

        self._fila_progresso: queue.Queue[float] = queue.Queue()
        self._fila_resultados: queue.Queue[dict] = queue.Queue()
        self._fila_status: queue.Queue[str] = queue.Queue()
        self._fila_erros: queue.Queue[dict[str, str]] = queue.Queue()
        self._resultado_atual: dict | None = None
        self._janela_tutorial = None
        self._janela_sobre = None
        self._janela_resultados = None
        self._itens_workspace: list[ctk.CTkLabel] = []
        self._item_workspace_selecionado: ctk.CTkLabel | None = None
        self._processando = False
        self._borda_padrao = "#3B8ED0"
        self._borda_erro = "#C62828"

        self._build()
        self.after_idle(self._centralizar_janela)
        self.after(100, self._processar_filas)

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        cabecalho = ctk.CTkFrame(self)
        cabecalho.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        cabecalho.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            cabecalho,
            text="EmerCalc",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(
            cabecalho,
            text="Importe a rede, execute o cálculo e exporte os resultados com segurança.",
            text_color="#C9D1D9",
            anchor="w",
            justify="left",
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

        barra = ctk.CTkFrame(self)
        barra.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        for coluna in range(3):
            barra.grid_columnconfigure(coluna, weight=1)
        ctk.CTkButton(barra, text="Início", command=self._ir_para_inicio).grid(
            row=0, column=0, padx=(8, 4), pady=8, sticky="ew"
        )
        ctk.CTkButton(barra, text="Tutorial", command=self._abrir_tutorial).grid(
            row=0, column=1, padx=4, pady=8, sticky="ew"
        )
        ctk.CTkButton(barra, text="Sobre", command=self._abrir_sobre).grid(
            row=0, column=2, padx=(4, 8), pady=8, sticky="ew"
        )

        workspace = ctk.CTkFrame(self)
        workspace.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))
        workspace.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(workspace, text="Workspace", width=110, anchor="w").grid(
            row=0, column=0, padx=(8, 6), pady=8
        )
        self.entrada_workspace = ctk.CTkEntry(workspace, textvariable=self.workspace_var, state="readonly")
        self.entrada_workspace.grid(row=0, column=1, sticky="ew", padx=(0, 6), pady=8)
        ctk.CTkButton(workspace, text="Navegar", command=self._selecionar_workspace).grid(
            row=0, column=2, padx=(0, 8), pady=8
        )

        body = ctk.CTkFrame(self)
        body.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        body.grid_columnconfigure(0, weight=0, minsize=270)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        esquerda = ctk.CTkFrame(body)
        esquerda.grid(row=0, column=0, sticky="nsew", padx=(8, 6), pady=8)
        esquerda.grid_rowconfigure(1, weight=1)
        esquerda.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(esquerda, text="Arquivos do workspace", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=8, pady=(8, 4)
        )
        self.lista = ctk.CTkScrollableFrame(esquerda)
        self.lista.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        direita = ctk.CTkFrame(body)
        direita.grid(row=0, column=1, sticky="nsew", padx=(6, 8), pady=8)
        direita.grid_columnconfigure(0, weight=1)
        direita.grid_rowconfigure(1, weight=1)

        self.tabs = ctk.CTkTabview(direita)
        self.tabs.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        self.tabs.add("Cálculo Completo")
        aba = self.tabs.tab("Cálculo Completo")
        aba.grid_columnconfigure(1, weight=1)

        self.entrada_grafo, self._linha_grafo = self._criar_linha_arquivo(
            aba,
            0,
            "Arquivo de Rede (CSV)",
            self.graph_var,
            ("CSV", "*.csv"),
            self._borda_padrao,
            lambda: self._validar_campo_arquivo(self.entrada_grafo, ".csv"),
        )
        self.entrada_uev, self._linha_uev = self._criar_linha_arquivo(
            aba,
            1,
            "Arquivo de UEVs (JSON)",
            self.uev_var,
            ("JSON", "*.json"),
            self._borda_padrao,
            lambda: self._validar_campo_arquivo(self.entrada_uev, ".json"),
        )

        linha_threshold = ctk.CTkFrame(aba)
        linha_threshold.grid(row=2, column=0, sticky="ew", padx=8, pady=4)
        linha_threshold.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(linha_threshold, text="Limiar de Propagação", width=180, anchor="w").grid(
            row=0, column=0, padx=(8, 6), pady=(8, 2)
        )
        self.entrada_threshold = ctk.CTkEntry(linha_threshold, textvariable=self.threshold_var)
        self.entrada_threshold.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=(8, 2))
        self.entrada_threshold.bind("<FocusOut>", lambda _event: self._validar_threshold())
        self.lbl_threshold_info = ctk.CTkLabel(
            linha_threshold,
            text="Valor numérico entre 0 e 1. Padrão: 0,1.",
            text_color="#C9D1D9",
            anchor="w",
            justify="left",
        )
        self.lbl_threshold_info.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(8, 8), pady=(0, 8))

        self.btn_iniciar = ctk.CTkButton(aba, text="Iniciar Cálculo", command=self._calcular)
        self.btn_iniciar.grid(row=3, column=0, sticky="ew", padx=8, pady=(12, 8))

        self.progresso = ctk.CTkProgressBar(aba)
        self.progresso.grid(row=4, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.progresso.set(0)

        botoes = ctk.CTkFrame(aba)
        botoes.grid(row=5, column=0, sticky="ew", padx=8, pady=(0, 8))
        for coluna in range(3):
            botoes.grid_columnconfigure(coluna, weight=1)
        self.btn_csv = ctk.CTkButton(
            botoes, text="Exportar CSV", state="disabled", command=lambda: self._exportar("csv")
        )
        self.btn_pdf = ctk.CTkButton(
            botoes, text="Exportar PDF", state="disabled", command=lambda: self._exportar("pdf")
        )
        self.btn_png = ctk.CTkButton(
            botoes, text="Exportar Grafo (PNG)", state="disabled", command=lambda: self._exportar("png")
        )
        self.btn_csv.grid(row=0, column=0, padx=4, pady=8, sticky="ew")
        self.btn_pdf.grid(row=0, column=1, padx=4, pady=8, sticky="ew")
        self.btn_png.grid(row=0, column=2, padx=4, pady=8, sticky="ew")

        self.log = ctk.CTkTextbox(aba, height=170, wrap="word")
        self.log.grid(row=6, column=0, sticky="nsew", padx=8, pady=(0, 8))
        aba.grid_rowconfigure(6, weight=1)
        self.log.configure(state="disabled")

    def _criar_linha_arquivo(
        self,
        pai,
        linha: int,
        rotulo: str,
        var: ctk.StringVar,
        tipo_arquivo: tuple[str, str],
        borda_padrao: str,
        validar_callback,
    ) -> tuple[ctk.CTkEntry, ctk.CTkFrame]:
        frame = ctk.CTkFrame(pai)
        frame.grid(row=linha, column=0, sticky="ew", padx=8, pady=4)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=rotulo, width=180, anchor="w").grid(
            row=0, column=0, padx=(8, 6), pady=8
        )
        entrada = ctk.CTkEntry(frame, textvariable=var, border_color=borda_padrao)
        entrada.grid(row=0, column=1, sticky="ew", padx=(0, 6), pady=8)
        entrada.bind("<FocusOut>", lambda _event: validar_callback())
        ctk.CTkButton(
            frame,
            text="Navegar",
            command=lambda: self._buscar_arquivo(var, tipo_arquivo[0].lower(), tipo_arquivo[1]),
        ).grid(row=0, column=2, padx=(0, 8), pady=8)
        return entrada, frame

    def _centralizar_janela(self) -> None:
        self.update_idletasks()
        largura = self._largura_janela
        altura = self._altura_janela
        tela_largura = self.winfo_screenwidth()
        tela_altura = self.winfo_screenheight()
        x = max(0, (tela_largura - largura) // 2)
        y = max(0, (tela_altura - altura) // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def _ir_para_inicio(self) -> None:
        self.lift()
        self.focus_force()
        self._log("Tela inicial selecionada.")

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

        arquivos = []
        for item in sorted(Path(caminho).iterdir(), key=lambda p: p.name.lower()):
            if item.is_file() and item.suffix.lower() in {".csv", ".json"}:
                prefixo = "[CSV]" if item.suffix.lower() == ".csv" else "[JSON]"
                arquivos.append((prefixo, item))

        for prefixo, arquivo in arquivos:
            label = ctk.CTkLabel(
                self.lista,
                text=f"{prefixo} {arquivo.name}",
                anchor="w",
                justify="left",
                corner_radius=6,
                cursor="hand2",
            )
            label._arquivo_nome = arquivo.name  # type: ignore[attr-defined]
            label.bind("<Button-1>", self._carregar_selecionado)
            label.pack(fill="x", padx=4, pady=3)
            self._itens_workspace.append(label)

        if not self._itens_workspace:
            vazio = ctk.CTkLabel(
                self.lista,
                text="Nenhum arquivo CSV ou JSON encontrado.",
                anchor="w",
                justify="left",
            )
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
            self._validar_campo_arquivo(self.entrada_grafo, ".csv")
            self._log(f"Arquivo de rede selecionado: {caminho.name}")
        elif caminho.suffix.lower() == ".json":
            self.uev_var.set(str(caminho))
            self._validar_campo_arquivo(self.entrada_uev, ".json")
            self._log(f"Arquivo de UEVs selecionado: {caminho.name}")

    def _buscar_arquivo(self, var: ctk.StringVar, descricao: str, padrao: str) -> None:
        caminho = filedialog.askopenfilename(
            initialdir=self.workspace_var.get() or None,
            filetypes=[(f"Arquivos {descricao.upper()}", padrao), ("Arquivos suportados", "*.csv *.json")],
        )
        if caminho:
            var.set(caminho)
            if descricao == "csv":
                self._validar_campo_arquivo(self.entrada_grafo, ".csv")
            else:
                self._validar_campo_arquivo(self.entrada_uev, ".json")
            self._log(f"Arquivo selecionado: {Path(caminho).name}")

    def _validar_campo_arquivo(self, entrada: ctk.CTkEntry, extensao: str) -> bool:
        valor = entrada.get().strip()
        valido = bool(valor) and Path(valor).suffix.lower() == extensao and Path(valor).is_file()
        entrada.configure(border_color=self._borda_padrao if valido else self._borda_erro)
        return valido

    def _validar_threshold(self, silencioso: bool = False) -> bool:
        valor_texto = self.threshold_var.get().strip().replace(",", ".")
        try:
            valor = float(valor_texto)
        except ValueError:
            self.entrada_threshold.configure(border_color=self._borda_erro)
            self.lbl_threshold_info.configure(text="Informe um valor numérico entre 0 e 1.", text_color="#FF6B6B")
            if not silencioso:
                self._log("[ERRO] Limiar inválido informado.")
            return False

        if not 0 < valor <= 1:
            self.entrada_threshold.configure(border_color=self._borda_erro)
            self.lbl_threshold_info.configure(text="O limiar precisa estar entre 0 e 1.", text_color="#FF6B6B")
            if not silencioso:
                self._log("[ERRO] Limiar fora do intervalo permitido.")
            return False

        self.entrada_threshold.configure(border_color=self._borda_padrao)
        self.lbl_threshold_info.configure(text="Valor numérico entre 0 e 1. Padrão: 0,1.", text_color="#C9D1D9")
        return True

    def _validar_antes_de_calcular(self) -> bool:
        faltantes = []
        if not self.graph_var.get().strip():
            faltantes.append("arquivo CSV da rede")
        if not self.uev_var.get().strip():
            faltantes.append("arquivo JSON de UEVs")
        if faltantes:
            mostrar_erro(
                self,
                "Campos obrigatórios",
                "Preencha os campos de entrada antes de iniciar o cálculo.",
                "O sistema precisa de um CSV da rede e de um JSON de UEVs para processar a análise.",
                "Selecione os arquivos manualmente ou use o workspace para preencher os campos automaticamente.",
            )
            self._log("[ERRO] Tentativa de cálculo com campos vazios.")
            return False
        if not self._validar_threshold(silencioso=True):
            mostrar_erro(
                self,
                "Limiar inválido",
                "O limiar informado não pode ser usado no cálculo.",
                "O valor precisa ser numérico e estar entre 0 e 1.",
                "Corrija o campo de limiar e tente novamente.",
            )
            self._log("[ERRO] Tentativa de cálculo com limiar inválido.")
            return False
        return True

    def _calcular(self) -> None:
        self._validar_campo_arquivo(self.entrada_grafo, ".csv")
        self._validar_campo_arquivo(self.entrada_uev, ".json")
        if not self._validar_antes_de_calcular():
            return

        self._resultado_atual = None
        self.btn_csv.configure(state="disabled")
        self.btn_pdf.configure(state="disabled")
        self.btn_png.configure(state="disabled")
        self.progresso.set(0)
        self._definir_estado_processamento(True)
        self._log("Iniciando cálculo...")

        params = {
            "caminho_grafo": self.graph_var.get(),
            "caminho_uevs": self.uev_var.get(),
            "threshold": self.threshold_var.get() or "0.1",
            "callback": lambda progresso: self._fila_progresso.put(progresso),
        }
        self.controller.iniciar_calculo(
            params,
            on_done=lambda resultados: self._fila_resultados.put(resultados),
            on_status=lambda mensagem: self._fila_status.put(mensagem),
            on_error=lambda erro: self._fila_erros.put(erro),
        )

    def _definir_estado_processamento(self, ativo: bool) -> None:
        self._processando = ativo
        self.btn_iniciar.configure(text="Calculando..." if ativo else "Iniciar Cálculo", state="disabled" if ativo else "normal")

    def _processar_filas(self) -> None:
        while not self._fila_status.empty():
            self._log(self._fila_status.get())

        while not self._fila_progresso.empty():
            progresso = float(self._fila_progresso.get())
            self.progresso.set(progresso / 100.0 if progresso > 1 else progresso)

        while not self._fila_resultados.empty():
            self._resultado_atual = self._fila_resultados.get()
            if self._janela_resultados is not None and self._janela_resultados.winfo_exists():
                self._janela_resultados.destroy()
            self._janela_resultados = ResultsWindow(self, resultados=self._resultado_atual)
            self.btn_csv.configure(state="normal")
            self.btn_pdf.configure(state="normal")
            self.btn_png.configure(state="normal")
            self._definir_estado_processamento(False)
            self._log("Cálculo concluído.")

        while not self._fila_erros.empty():
            erro = self._fila_erros.get()
            self._definir_estado_processamento(False)
            self.progresso.set(0)
            self.btn_csv.configure(state="disabled")
            self.btn_pdf.configure(state="disabled")
            self.btn_png.configure(state="disabled")
            texto_erro = erro.get("mensagem", "O cálculo falhou.")
            self._log(f"[ERRO] {texto_erro}")
            mostrar_erro(
                self,
                erro.get("titulo", "Erro"),
                erro.get("mensagem", "O cálculo encontrou um problema."),
                erro.get("explicacao", texto_erro),
                erro.get("solucao", "Revise os dados de entrada e tente novamente."),
            )

        self.after(100, self._processar_filas)

    def _abrir_tutorial(self) -> None:
        if self._janela_tutorial is not None and self._janela_tutorial.winfo_exists():
            self._janela_tutorial.lift()
            self._janela_tutorial.focus_force()
            return
        self._janela_tutorial = TutorialWindow(self)

    def _abrir_sobre(self) -> None:
        if self._janela_sobre is not None and self._janela_sobre.winfo_exists():
            self._janela_sobre.lift()
            self._janela_sobre.focus_force()
            return
        self._janela_sobre = AboutWindow(self)

    def _exportar(self, tipo: str) -> None:
        if not self._resultado_atual:
            mostrar_erro(
                self,
                "Nenhum resultado",
                "Não há resultados disponíveis para exportação.",
                "Execute um cálculo com sucesso antes de exportar CSV, PDF ou PNG.",
                "Clique em \"Iniciar Cálculo\" e aguarde a abertura da janela de resultados.",
            )
            self._log("[ERRO] Exportação solicitada sem resultados disponíveis.")
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
        if not caminho:
            return

        try:
            self.controller.ultimos_resultados = self._resultado_atual
            self.controller.exportar_resultados(tipo, caminho)
        except Exception as exc:
            mostrar_erro(
                self,
                "Falha na exportação",
                "Não foi possível salvar o arquivo solicitado.",
                str(exc),
                "Verifique se o caminho é válido, se você tem permissão de escrita e tente novamente.",
            )
            self._log(f"[ERRO] Falha ao exportar {tipo.upper()}: {exc}")
            return

        self._log(f"Exportado: {caminho}")

    def _ao_fechar(self) -> None:
        self.destroy()

    def _log(self, mensagem: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"{mensagem}\n")
        self.log.see("end")
        self.log.configure(state="disabled")
