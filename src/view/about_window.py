"""Janela about."""

from __future__ import annotations

import tkinter as tk


class AboutWindow(tk.Toplevel):
    """Mostra informações do projeto."""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("About")
        label = tk.Label(
            self,
            text="APS de Engenharia de Software\nSistema de cálculo de emergia\nReferências: Odum, Marvuglia et al.",
            justify="left",
        )
        label.pack(padx=12, pady=12)

