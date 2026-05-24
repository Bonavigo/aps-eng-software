"""Janela about."""

from __future__ import annotations

import customtkinter as ctk


class AboutWindow(ctk.CTkToplevel):
    """Mostra informações do projeto."""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("Sobre - EmerCalc")
        self.geometry("620x420")
        self.transient(master)
        self.after_idle(self._centralizar_janela)

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            container,
            text="EmerCalc",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))
        ctk.CTkLabel(
            container,
            text="Sistema de cálculo de emergia para redes LCI.",
            font=ctk.CTkFont(size=14),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=4)
        ctk.CTkLabel(
            container,
            text="Disciplina: Engenharia de Software",
            anchor="w",
            justify="left",
        ).grid(row=2, column=0, sticky="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            container,
            text="Curso: Análise e Desenvolvimento de Sistemas",
            anchor="w",
            justify="left",
        ).grid(row=3, column=0, sticky="w", padx=12, pady=2)
        ctk.CTkLabel(
            container,
            text="Instituição: Projeto acadêmico APS",
            anchor="w",
            justify="left",
        ).grid(row=4, column=0, sticky="w", padx=12, pady=2)

        referencia = (
            "Referência ABNT:\n"
            "ODUM, Howard T. Environmental Accounting: Emergy and Environmental Decision Making. "
            "New York: John Wiley & Sons, 1996.\n"
            "MARVUGLIA, Antonino et al. SCALE: Software for CALculating Emergy based on Life Cycle Inventories. 2013.\n"
            "ARBAULT, Damien et al. Emergy evaluation using the calculation software SCALE. 2014."
        )
        ctk.CTkLabel(
            container,
            text=referencia,
            justify="left",
            anchor="w",
            wraplength=560,
        ).grid(row=5, column=0, sticky="w", padx=12, pady=(10, 12))

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
