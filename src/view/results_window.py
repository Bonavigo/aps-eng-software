"""Janela de resultados."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ResultsWindow(tk.Toplevel):
    """Exibe resultados em tabela."""

    def __init__(self, master=None, resultados=None) -> None:
        super().__init__(master)
        self.title("Resultados")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        tree = ttk.Treeview(container, columns=("proc", "emergia", "pct"), show="headings", height=8)
        for col, titulo in [("proc", "Processo"), ("emergia", "Emergia (sej)"), ("pct", "% Contribuição")]:
            tree.heading(col, text=titulo)
            tree.column(col, width=180 if col == "proc" else 140, anchor="center")
        tree.pack(fill="x", expand=False)
        for processo, dados in (resultados or {}).get("contribuicoes", {}).items():
            tree.insert("", "end", values=(processo, dados["emergia"], f"{dados['percentual']:.2f}"))

        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        nomes = list((resultados or {}).get("contribuicoes", {}).keys())
        valores = [dados["percentual"] for dados in (resultados or {}).get("contribuicoes", {}).values()]
        ax.bar(nomes, valores, color="#1565c0")
        ax.set_ylabel("%")
        ax.set_title("Contribuição por fonte")
        ax.tick_params(axis="x", labelrotation=30)
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
