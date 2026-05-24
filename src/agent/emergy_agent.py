"""Agente de coordenação do cálculo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.model.emergy_calculator import EmergiaCalculator
from src.model.graph_builder import GraphBuilder
from src.model.lci_manager import LCIManager

from cthinker import Agent, Pipeline, Step


@dataclass
class EmergiaAgent:
    """Coordena o pipeline de cálculo."""

    manager: LCIManager
    builder: GraphBuilder
    calculator: EmergiaCalculator

    def __init__(self) -> None:
        self.manager = LCIManager()
        self.builder = GraphBuilder()
        self.calculator = EmergiaCalculator()
        self.pipeline = Pipeline(
            [
                Step("carregar_dados", self._carregar_dados),
                Step("validar_dados", self._validar_dados),
                Step("construir_grafo", self._construir_grafo),
                Step("calcular_emergia", self._calcular_emergia),
                Step("gerar_resultados", self._gerar_resultados),
            ]
        )

    def executar(self, caminho_grafo: str, caminho_uevs: str, threshold: float, callback=None) -> dict[str, Any]:
        contexto = {
            "caminho_grafo": caminho_grafo,
            "caminho_uevs": caminho_uevs,
            "threshold": threshold,
            "callback": callback,
        }
        return self.pipeline.run(contexto)["resultados"]

    def _carregar_dados(self, contexto: dict[str, Any]) -> dict[str, Any]:
        contexto["dados"] = self.manager.carregar_csv(contexto["caminho_grafo"])
        contexto["uevs"] = self.manager.carregar_uevs(contexto["caminho_uevs"])
        return contexto

    def _validar_dados(self, contexto: dict[str, Any]) -> dict[str, Any]:
        self.manager.validar_dados(contexto["dados"])
        return contexto

    def _construir_grafo(self, contexto: dict[str, Any]) -> dict[str, Any]:
        contexto["grafo"] = self.builder.construir_grafo(contexto["dados"], contexto["uevs"])
        return contexto

    def _calcular_emergia(self, contexto: dict[str, Any]) -> dict[str, Any]:
        contexto["resultados"] = self.calculator.calcular(
            contexto["grafo"],
            threshold=float(contexto.get("threshold", 0.1)),
            callback=contexto.get("callback"),
        )
        contexto["resultados"]["grafo"] = contexto["grafo"]
        return contexto

    def _gerar_resultados(self, contexto: dict[str, Any]) -> dict[str, Any]:
        return contexto
