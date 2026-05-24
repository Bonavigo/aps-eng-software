"""Janela de tutorial."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class TutorialWindow(tk.Toplevel):
    """Janela com explicação do sistema."""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("Tutorial")
        texto = tk.Text(self, wrap="word", width=80, height=25)
        texto.insert(
            "1.0",
            "Emergia e um conceito de H.T. Odum para medir energia solar equivalente.\n\n"
            "Regra 1: nao dupla contagem.\nRegra 2: coprodutos recebem a emergia inteira.\n"
            "Regra 3: splits distribuem proporcionalmente.\nRegra 4: ciclos devem ser evitados.\n",
        )
        texto.configure(state="disabled")
        texto.pack(fill="both", expand=True, padx=8, pady=8)

