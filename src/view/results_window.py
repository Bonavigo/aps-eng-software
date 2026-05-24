"""Janela de resultados."""

from __future__ import annotations

import customtkinter as ctk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ResultsWindow(ctk.CTkToplevel):
    """Exibe resultados em tabela e gráfico."""

    def __init__(self, master=None, resultados=None) -> None:
        super().__init__(master)
        self.title("Resultados - EmerCalc")
        self.geometry("1050x760")
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after_idle(self._centralizar_janela)

        self._resultados = resultados or {}

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            container,
            text="Resultados",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        tabela_frame = ctk.CTkFrame(container)
        tabela_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        tabela_frame.grid_columnconfigure(0, weight=1)
        tabela_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Results.Treeview",
            background="#1E1E1E",
            fieldbackground="#1E1E1E",
            foreground="#F2F2F2",
            rowheight=28,
            bordercolor="#2B2B2B",
            lightcolor="#2B2B2B",
            darkcolor="#2B2B2B",
        )
        style.configure(
            "Results.Treeview.Heading",
            background="#2A2A2A",
            foreground="#FFFFFF",
            relief="flat",
        )
        style.map("Results.Treeview.Heading", background=[("active", "#3B3B3B")])

        tree = ttk.Treeview(
            tabela_frame,
            columns=("proc", "emergia", "pct"),
            show="headings",
            height=8,
            style="Results.Treeview",
        )
        for col, titulo, largura in [
            ("proc", "Processo", 420),
            ("emergia", "Emergia (sej)", 220),
            ("pct", "Contribuição (%)", 220),
        ]:
            tree.heading(col, text=titulo)
            tree.column(col, width=largura, anchor="center", stretch=True)

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)

        contribuicoes = self._resultados.get("contribuicoes", {})
        for processo, dados in contribuicoes.items():
            tree.insert(
                "",
                "end",
                values=(processo, f"{dados['emergia']:.6f}", f"{dados['percentual']:.2f} %"),
            )

        grafico_frame = ctk.CTkFrame(container)
        grafico_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))
        grafico_frame.grid_columnconfigure(0, weight=1)
        grafico_frame.grid_rowconfigure(0, weight=1)

        fig = Figure(figsize=(8, 4.2), dpi=100, facecolor="#1E1E1E")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1E1E1E")

        nomes = list(contribuicoes.keys())
        valores = [dados["percentual"] for dados in contribuicoes.values()]
        if nomes:
            if len(nomes) > 10:
                ax.barh(nomes, valores, color="#5AA9E6")
                ax.invert_yaxis()
                ax.set_xlabel("Contribuição (%)", color="#F2F2F2")
            else:
                ax.bar(nomes, valores, color="#5AA9E6")
                ax.set_ylabel("Contribuição (%)", color="#F2F2F2")
                ax.tick_params(axis="x", labelrotation=30)
            ax.set_title("Contribuição por Fonte (%)", color="#F2F2F2")
            ax.tick_params(colors="#F2F2F2")
            for spine in ax.spines.values():
                spine.set_color("#F2F2F2")
        else:
            ax.text(0.5, 0.5, "Nenhuma contribuição disponível.", ha="center", va="center", color="#F2F2F2")
            ax.set_axis_off()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        ctk.CTkButton(container, text="Fechar", command=self.destroy).grid(
            row=3, column=0, sticky="e", padx=8, pady=(0, 8)
        )

    def _centralizar_janela(self) -> None:
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        if self.master is not None:
            master_x = self.master.winfo_rootx()
            master_y = self.master.winfo_rooty()
            master_largura = self.master.winfo_width()
            master_altura = self.master.winfo_height()
            x = max(0, master_x + (master_largura - largura) // 2)
            y = max(0, master_y + (master_altura - altura) // 2)
        else:
            tela_largura = self.winfo_screenwidth()
            tela_altura = self.winfo_screenheight()
            x = max(0, (tela_largura - largura) // 2)
            y = max(0, (tela_altura - altura) // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
