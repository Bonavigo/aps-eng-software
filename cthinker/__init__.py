"""Shim local compatível com a API usada pelo projeto.

Se a biblioteca externa `cthinker` estiver disponível no ambiente,
ela pode substituir este módulo sem mudanças no resto do código.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class Step:
    """Etapa única do pipeline."""

    name: str
    fn: Callable[[dict[str, Any]], dict[str, Any]]


class Pipeline:
    """Executa steps em sequência passando o contexto adiante."""

    def __init__(self, steps: Iterable[Step]) -> None:
        self.steps = list(steps)

    def run(self, contexto: dict[str, Any]) -> dict[str, Any]:
        for step in self.steps:
            contexto = step.fn(contexto)
            if not isinstance(contexto, dict):
                raise TypeError(f"Step '{step.name}' deve retornar um dict.")
        return contexto


class Agent:
    """Compatibilidade mínima com a API esperada."""

    def __init__(self, pipeline: Pipeline) -> None:
        self.pipeline = pipeline

    def run(self, contexto: dict[str, Any]) -> dict[str, Any]:
        return self.pipeline.run(contexto)

