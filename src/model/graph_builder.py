"""Construção do grafo de processos."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None


@dataclass
class SimpleDiGraph:
    """Grafo dirigido simples para fallback sem networkx."""

    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: dict[tuple[str, str], dict[str, Any]] = field(default_factory=dict)

    def add_node(self, node_id: str, **attrs: Any) -> None:
        self.nodes[node_id] = {**self.nodes.get(node_id, {}), **attrs}

    def add_edge(self, origem: str, destino: str, **attrs: Any) -> None:
        self.edges[(origem, destino)] = attrs

    def predecessors(self, node: str) -> list[str]:
        return [o for (o, d) in self.edges if d == node]

    def successors(self, node: str) -> list[str]:
        return [d for (o, d) in self.edges if o == node]

    def has_node(self, node: str) -> bool:
        return node in self.nodes


class GraphBuilder:
    """Constrói o grafo a partir dos dados LCI."""

    def __init__(self) -> None:
        self._grafo = None

    def construir_grafo(self, dados: dict[str, list[dict[str, Any]]], uevs: dict[str, float]) -> Any:
        grafo = nx.DiGraph() if nx else SimpleDiGraph()
        for processo in dados.get("processos", []):
            node_id = str(processo.get("processo_id") or processo.get("id"))
            grafo.add_node(
                node_id,
                id=node_id,
                nome=processo.get("nome", node_id),
                tipo=processo.get("tipo", "processo"),
                uev=uevs.get(node_id),
            )
        for fluxo in dados.get("fluxos", []):
            grafo.add_edge(
                str(fluxo["origem"]),
                str(fluxo["destino"]),
                quantidade=float(fluxo["quantidade"]),
                unidade=fluxo.get("unidade", ""),
            )
        self._grafo = grafo
        return grafo

    def obter_fontes(self) -> list[str]:
        if self._grafo is None:
            return []
        if nx and hasattr(self._grafo, "in_degree"):
            return [n for n, grau in self._grafo.in_degree() if grau == 0]
        return [n for n in self._grafo.nodes if not self._grafo.predecessors(n)]

    def obter_produtos(self) -> list[str]:
        if self._grafo is None:
            return []
        if nx and hasattr(self._grafo, "out_degree"):
            return [n for n, grau in self._grafo.out_degree() if grau == 0]
        return [n for n in self._grafo.nodes if not self._grafo.successors(n)]

