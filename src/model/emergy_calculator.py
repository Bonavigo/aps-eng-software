"""Cálculo de emergia por backtracking em grafo."""

from __future__ import annotations

from collections import defaultdict
from time import perf_counter
from typing import Any, Callable


ProgressCallback = Callable[[float], None]


class EmergiaCalculator:
    """Calcula emergia a partir de um grafo dirigido."""

    def calcular(self, grafo: Any, threshold: float = 0.1, callback: ProgressCallback | None = None) -> dict[str, Any]:
        """Executa o cálculo principal."""
        inicio = perf_counter()
        produtos = self._obter_produtos(grafo)
        fontes = self._obter_fontes(grafo)
        contribuicoes = defaultdict(float)
        caminhos_explorados = 0
        em_lost_threshold = 0.0
        em_lost_loops = 0.0
        total_meta = max(1, len(fontes) * max(1, len(produtos)))

        for fonte in fontes:
            uev = self._uev_do_no(grafo, fonte)
            total_saida = self._quantidade_saida_total(grafo, fonte)
            if uev <= 0 or total_saida <= 0:
                continue
            emergia_inicial = uev * total_saida
            contadores = {
                "caminhos_explorados": caminhos_explorados,
                "em_lost_threshold": em_lost_threshold,
                "em_lost_loops": em_lost_loops,
            }
            self._dfs(
                grafo=grafo,
                no_atual=fonte,
                emergia_atual=emergia_inicial,
                fonte=fonte,
                threshold=threshold,
                contribuicoes=contribuicoes,
                contador=contadores,
                visitados={fonte},
                callback=callback,
                total_meta=total_meta,
            )
            caminhos_explorados = int(contadores["caminhos_explorados"])
            em_lost_threshold = float(contadores["em_lost_threshold"])
            em_lost_loops = float(contadores["em_lost_loops"])

        emergia_total = float(sum(contribuicoes.values()))
        resultado = {
            "emergia_total": emergia_total,
            "uev_produto": emergia_total / self._quantidade_referencia_produto(grafo, produtos[0]) if produtos else emergia_total,
            "contribuicoes": {
                fonte: {"emergia": valor, "percentual": (valor / emergia_total * 100.0) if emergia_total else 0.0}
                for fonte, valor in contribuicoes.items()
            },
            "caminhos_explorados": caminhos_explorados,
            "em_lost_threshold": em_lost_threshold,
            "em_lost_loops": em_lost_loops,
            "tempo_calculo_s": perf_counter() - inicio,
        }
        return resultado

    def _dfs(
        self,
        grafo: Any,
        no_atual: str,
        emergia_atual: float,
        fonte: str,
        threshold: float,
        contribuicoes: defaultdict[str, float],
        contador: dict[str, float | int],
        visitados: set[str],
        callback: ProgressCallback | None,
        total_meta: int,
    ) -> None:
        if self._eh_produto(grafo, no_atual) or not self._sucessores(grafo, no_atual):
            contribuicoes[fonte] += emergia_atual
            contador["caminhos_explorados"] = int(contador["caminhos_explorados"]) + 1
            if callback:
                callback(min(1.0, int(contador["caminhos_explorados"]) / total_meta))
            return

        for sucessor, dados_aresta in self._sucessores_com_atributos(grafo, no_atual):
            if sucessor in visitados:
                contador["em_lost_loops"] = float(contador["em_lost_loops"]) + (emergia_atual * self._fracao_aresta(grafo, no_atual, sucessor, dados_aresta))
                continue

            fracao = self._fracao_aresta(grafo, no_atual, sucessor, dados_aresta)
            if fracao <= 0:
                continue

            emergia_proxima = emergia_atual * fracao
            if emergia_proxima < threshold:
                contador["em_lost_threshold"] = float(contador["em_lost_threshold"]) + emergia_proxima
                continue

            self._dfs(
                grafo=grafo,
                no_atual=sucessor,
                emergia_atual=emergia_proxima,
                fonte=fonte,
                threshold=threshold,
                contribuicoes=contribuicoes,
                contador=contador,
                visitados=visitados | {sucessor},
                callback=callback,
                total_meta=total_meta,
            )

    def _obter_fontes(self, grafo: Any) -> list[str]:
        if hasattr(grafo, "nodes"):
            fontes = [n for n, attrs in self._iter_nodes(grafo) if str(attrs.get("tipo", "")).lower() == "fonte"]
            if fontes:
                return fontes
        if hasattr(grafo, "in_degree"):
            return [n for n, grau in grafo.in_degree() if grau == 0]
        return [n for n in grafo.nodes if not grafo.predecessors(n)]

    def _obter_produtos(self, grafo: Any) -> list[str]:
        if hasattr(grafo, "nodes"):
            produtos = [
                n
                for n, attrs in self._iter_nodes(grafo)
                if str(attrs.get("tipo", "")).lower() in {"produto", "produto_final"}
            ]
            if produtos:
                return produtos
        if hasattr(grafo, "out_degree"):
            return [n for n, grau in grafo.out_degree() if grau == 0]
        return [n for n in grafo.nodes if not grafo.successors(n)]

    def _eh_produto(self, grafo: Any, no: str) -> bool:
        attrs = self._node_attrs(grafo, no)
        tipo = str(attrs.get("tipo", "")).lower()
        if tipo in {"produto", "produto_final"}:
            return True
        return not self._sucessores(grafo, no)

    def _uev_do_no(self, grafo: Any, no: str) -> float:
        attrs = self._node_attrs(grafo, no)
        valor = attrs.get("uev")
        if valor is None:
            return 0.0
        try:
            return float(valor)
        except (TypeError, ValueError):
            return 0.0

    def _quantidade_saida_total(self, grafo: Any, no: str) -> float:
        total = 0.0
        for sucessor, dados_aresta in self._sucessores_com_atributos(grafo, no):
            total += float(dados_aresta.get("quantidade", 0.0))
        return total

    def _quantidade_referencia_produto(self, grafo: Any, no: str) -> float:
        attrs = self._node_attrs(grafo, no)
        for chave in ("quantidade_ref", "quantidade", "referencia", "unidade_funcional"):
            valor = attrs.get(chave)
            if valor not in (None, ""):
                try:
                    return float(valor)
                except (TypeError, ValueError):
                    continue
        return 1.0

    def _fracao_aresta(self, grafo: Any, origem: str, destino: str, dados_aresta: dict[str, Any]) -> float:
        if str(dados_aresta.get("tipo_saida", "")).lower() == "coproduto":
            return 1.0
        fracao = dados_aresta.get("fracao")
        if fracao is not None:
            try:
                return float(fracao)
            except (TypeError, ValueError):
                pass
        total = self._quantidade_saida_total(grafo, origem)
        if total <= 0:
            return 0.0
        return float(dados_aresta.get("quantidade", 0.0)) / total

    def _sucessores(self, grafo: Any, no: str) -> list[str]:
        if hasattr(grafo, "successors"):
            return list(grafo.successors(no))
        return []

    def _sucessores_com_atributos(self, grafo: Any, no: str) -> list[tuple[str, dict[str, Any]]]:
        sucessores = self._sucessores(grafo, no)
        if hasattr(grafo, "get_edge_data"):
            return [(succ, grafo.get_edge_data(no, succ) or {}) for succ in sucessores]
        return [(succ, grafo.edges[(no, succ)]) for succ in sucessores]

    def _node_attrs(self, grafo: Any, no: str) -> dict[str, Any]:
        if hasattr(grafo, "nodes"):
            return grafo.nodes[no]
        return {}

    def _iter_nodes(self, grafo: Any) -> list[tuple[str, dict[str, Any]]]:
        if hasattr(grafo, "nodes") and callable(getattr(grafo, "nodes", None)):
            return list(grafo.nodes(data=True))
        if hasattr(grafo, "nodes"):
            return list(grafo.nodes.items())
        return []
