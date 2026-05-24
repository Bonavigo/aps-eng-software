"""Cálculo de emergia por backtracking em grafo."""

from __future__ import annotations

from collections import defaultdict
from time import perf_counter
from typing import Any, Callable


ProgressCallback = Callable[[float], None]


class EmergiaCalculator:
    """Calcula emergia a partir de um grafo dirigido."""

    def calcular(self, grafo: Any, threshold: float = 0.1, callback: ProgressCallback | None = None) -> dict[str, Any]:
        """Executa o cálculo principal.

        Args:
            grafo: Grafo dirigido com nós e arestas.
            threshold: Limiar mínimo relativo.
            callback: Função de progresso.
        """
        inicio = perf_counter()
        produtos = self._obter_produtos(grafo)
        fontes = self._obter_fontes(grafo)
        contribuicoes = defaultdict(float)
        caminhos_explorados = 0
        visitados_cache: set[tuple[str, str]] = set()

        for produto in produtos:
            for fonte in fontes:
                for caminho, fator in self._caminhos_fonte_produto(grafo, fonte, produto, threshold):
                    chave = (fonte, produto)
                    if chave in visitados_cache:
                        continue
                    visitados_cache.add(chave)
                    uev = self._uev_do_no(grafo, fonte)
                    contribuicoes[fonte] += uev * fator
                    caminhos_explorados += 1
                    if callback:
                        callback(min(1.0, caminhos_explorados / max(1, len(fontes) * max(1, len(produtos)))))

        emergia_total = float(sum(contribuicoes.values()))
        resultado = {
            "emergia_total": emergia_total,
            "uev_produto": emergia_total,
            "contribuicoes": {
                fonte: {"emergia": valor, "percentual": (valor / emergia_total * 100.0) if emergia_total else 0.0}
                for fonte, valor in contribuicoes.items()
            },
            "caminhos_explorados": caminhos_explorados,
            "tempo_calculo_s": perf_counter() - inicio,
        }
        return resultado

    def _caminhos_fonte_produto(self, grafo: Any, fonte: str, produto: str, threshold: float) -> list[tuple[list[str], float]]:
        resultados: list[tuple[list[str], float]] = []

        def dfs(no_atual: str, caminho: list[str], fator: float, visitados: set[str]) -> None:
            if fator < threshold:
                return
            if no_atual == produto:
                resultados.append((caminho[:], fator))
                return
            for succ, attrs in self._successors_with_attrs(grafo, no_atual):
                if succ in visitados:
                    continue
                peso = float(attrs.get("quantidade", 1.0))
                dfs(succ, caminho + [succ], fator * peso, visitados | {succ})

        dfs(fonte, [fonte], 1.0, {fonte})
        return resultados

    def _obter_fontes(self, grafo: Any) -> list[str]:
        if hasattr(grafo, "in_degree"):
            return [n for n, grau in grafo.in_degree() if grau == 0]
        return [n for n in grafo.nodes if not grafo.predecessors(n)]

    def _obter_produtos(self, grafo: Any) -> list[str]:
        if hasattr(grafo, "out_degree"):
            return [n for n, grau in grafo.out_degree() if grau == 0]
        return [n for n in grafo.nodes if not grafo.successors(n)]

    def _uev_do_no(self, grafo: Any, no: str) -> float:
        attrs = grafo.nodes[no] if hasattr(grafo, "nodes") and isinstance(grafo.nodes, dict) else grafo.nodes[no]
        return float(attrs.get("uev") or 1.0)

    def _successors_with_attrs(self, grafo: Any, no: str) -> list[tuple[str, dict[str, Any]]]:
        if hasattr(grafo, "successors") and hasattr(grafo, "get_edge_data"):
            return [(succ, grafo.get_edge_data(no, succ) or {}) for succ in grafo.successors(no)]
        return [(succ, grafo.edges[(no, succ)]) for succ in grafo.successors(no)]
