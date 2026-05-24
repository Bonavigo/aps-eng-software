"""Diálogos reutilizáveis da interface."""

from __future__ import annotations

import customtkinter as ctk


def mostrar_erro(
    master,
    titulo: str,
    mensagem_curta: str,
    explicacao: str,
    como_resolver: str,
) -> ctk.CTkToplevel:
    """Exibe um modal de erro amigável e centralizado."""

    largura = 480
    altura = 320
    janela = ctk.CTkToplevel(master)
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.resizable(False, False)
    janela.transient(master)
    janela.grab_set()
    janela.protocol("WM_DELETE_WINDOW", janela.destroy)

    if master is not None:
        master.update_idletasks()
        janela.update_idletasks()
        x = max(0, master.winfo_rootx() + (master.winfo_width() - largura) // 2)
        y = max(0, master.winfo_rooty() + (master.winfo_height() - altura) // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    container = ctk.CTkFrame(janela)
    container.pack(fill="both", expand=True, padx=12, pady=12)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(
        container,
        text=mensagem_curta,
        text_color="#FF6B6B",
        font=ctk.CTkFont(size=16, weight="bold"),
        wraplength=420,
        justify="left",
        anchor="w",
    ).grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 10))

    texto = ctk.CTkTextbox(container, wrap="word")
    texto.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 10))
    texto.insert("end", f"{explicacao}\n\n{como_resolver}")
    texto.configure(state="disabled")

    ctk.CTkButton(container, text="Entendi", command=janela.destroy).grid(row=2, column=0, pady=(0, 8))
    return janela
