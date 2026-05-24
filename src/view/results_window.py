"""Janela de resultados."""

from __future__ import annotations

import customtkinter as ctk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ResultsWindow(ctk.CTkToplevel):
    """Exibe resultados em tabela."""

    def __init__(self, master=None, resultados=None) -> None:
        super().__init__(master)
        self.title("Resultados")
        self.geometry("900x600")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(container, text="Resultados", font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 4)
        )

        tabela_frame = ctk.CTkFrame(container)
        tabela_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        tabela_frame.grid_columnconfigure(0, weight=1)

        tree = ttk.Treeview(
            tabela_frame,
            columns=("proc", "emergia", "pct"),
            show="headings",
            height=8,
        )
        for col, titulo in [
            ("proc", "Processo"),
            ("emergia", "Emergia (sej)"),
            ("pct", "Contribuição (%)"),
        ]:
            tree.heading(col, text=titulo)
            tree.column(col, width=220 if col == "proc" else 160, anchor="center")
        tree.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        for processo, dados in (resultados or {}).get("contribuicoes", {}).items():
            tree.insert(
                "",
                "end",
                values=(processo, f"{dados['emergia']:.6f}", f"{dados['percentual']:.2f} %"),
            )

        grafico_frame = ctk.CTkFrame(container)
        grafico_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))
        grafico_frame.grid_columnconfigure(0, weight=1)
        grafico_frame.grid_rowconfigure(0, weight=1)

        fig = Figure(figsize=(6, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        contribuicoes = (resultados or {}).get("contribuicoes", {})
        nomes = list(contribuicoes.keys())
        valores = [dados["percentual"] for dados in contribuicoes.values()]
        ax.bar(nomes, valores, color="#1565c0")
        ax.set_ylabel("Contribuição (%)")
        ax.set_title("Contribuições por Fonte")
        ax.tick_params(axis="x", labelrotation=30)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
