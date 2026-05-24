"""Controlador da aplicação."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Callable

from src.agent.emergy_agent import EmergiaAgent
from src.utils.report_generator import ReportGenerator


class AppController:
    """Coordena cálculo, exportação e comunicação com a GUI."""

    def __init__(self) -> None:
        self.agent = EmergiaAgent()
        self.report = ReportGenerator()
        self.ultimos_resultados: dict[str, Any] | None = None
        self.ultima_entrada: dict[str, str] | None = None

    def iniciar_calculo(self, params: dict[str, Any], on_done: Callable[[dict[str, Any]], None] | None = None) -> threading.Thread:
        """Executa o cálculo em uma thread."""
        def tarefa() -> None:
            resultado = self.agent.executar(
                params["caminho_grafo"],
                params["caminho_uevs"],
                float(params.get("threshold", 0.1)),
                params.get("callback"),
            )
            self.ultimos_resultados = resultado
            self.ultima_entrada = params
            if on_done:
                on_done(resultado)

        thread = threading.Thread(target=tarefa, daemon=True)
        thread.start()
        return thread

    def exportar_resultados(self, tipo: str, caminho: str) -> None:
        if not self.ultimos_resultados:
            raise RuntimeError("Não há resultados para exportar.")
        if tipo == "csv":
            self.report.exportar_csv(self.ultimos_resultados, caminho)
        elif tipo == "pdf":
            self.report.exportar_pdf(self.ultimos_resultados, caminho)
        elif tipo == "png":
            self.report.exportar_grafo_png(self.ultimos_resultados.get("grafo"), caminho)
        else:
            raise ValueError(f"Tipo de exportação inválido: {tipo}")
