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
            tipo = str(processo.get("tipo", "processo")).strip().lower()
            if tipo == "produto_final":
                tipo = "produto"
            grafo.add_node(
                node_id,
                id=node_id,
                nome=processo.get("nome", node_id),
                tipo=tipo,
                uev=float(uevs[node_id]) if node_id in uevs else None,
            )
        for fluxo in dados.get("fluxos", []):
            grafo.add_edge(
                str(fluxo["origem"]),
                str(fluxo["destino"]),
                quantidade=float(fluxo["quantidade"]),
                unidade=fluxo.get("unidade", ""),
            )
        self._normalizar_fluxos(grafo)
        self._grafo = grafo
        return grafo

    def obter_fontes(self) -> list[str]:
        if self._grafo is None:
            return []
        fontes = [n for n, attrs in self._iter_nodes(self._grafo) if str(attrs.get("tipo", "")).lower() == "fonte"]
        if fontes:
            return fontes
        if nx and hasattr(self._grafo, "in_degree"):
            return [n for n, grau in self._grafo.in_degree() if grau == 0]
        return [n for n in self._grafo.nodes if not self._grafo.predecessors(n)]

    def obter_produtos(self) -> list[str]:
        if self._grafo is None:
            return []
        produtos = [n for n, attrs in self._iter_nodes(self._grafo) if str(attrs.get("tipo", "")).lower() in {"produto", "produto_final"}]
        if produtos:
            return produtos
        if nx and hasattr(self._grafo, "out_degree"):
            return [n for n, grau in self._grafo.out_degree() if grau == 0]
        return [n for n in self._grafo.nodes if not self._grafo.successors(n)]

    def _normalizar_fluxos(self, grafo: Any) -> None:
        """Calcula frações de saída e marca arestas por tipo de saída."""
        for no, attrs in self._iter_nodes(grafo):
            sucessores = list(grafo.successors(no))
            if not sucessores:
                continue
            total_saida = 0.0
            for succ in sucessores:
                dados_aresta = self._edge_data(grafo, no, succ)
                total_saida += float(dados_aresta.get("quantidade", 0.0))

            e_coproduto = bool(attrs.get("multi_output") or attrs.get("coproduto"))
            for succ in sucessores:
                dados_aresta = self._edge_data(grafo, no, succ)
                quantidade = float(dados_aresta.get("quantidade", 0.0))
                fracao = (quantidade / total_saida) if total_saida > 0 else 0.0
                dados_aresta["fracao"] = fracao
                dados_aresta["tipo_saida"] = "coproduto" if e_coproduto else "split"

    def _iter_nodes(self, grafo: Any) -> list[tuple[str, dict[str, Any]]]:
        if hasattr(grafo, "nodes") and callable(getattr(grafo, "nodes", None)):
            return list(grafo.nodes(data=True))
        if hasattr(grafo, "nodes"):
            return list(grafo.nodes.items())
        return []

    def _edge_data(self, grafo: Any, origem: str, destino: str) -> dict[str, Any]:
        if hasattr(grafo, "get_edge_data"):
            dados = grafo.get_edge_data(origem, destino)
            if dados is None:
                dados = {}
            return dados
        return grafo.edges[(origem, destino)]
