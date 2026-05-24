"""Janela about."""

from __future__ import annotations

import customtkinter as ctk


class AboutWindow(ctk.CTkToplevel):
    """Mostra informações do projeto."""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("Sobre")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            container,
            text="APS de Engenharia de Software",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=12, pady=(12, 4))
        ctk.CTkLabel(
            container,
            text="Sistema de cálculo de emergia",
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w", padx=12, pady=4)
        ctk.CTkLabel(
            container,
            text="Referências: Odum, Marvuglia et al.",
            justify="left",
            anchor="w",
            wraplength=360,
        ).pack(anchor="w", padx=12, pady=(4, 12))
