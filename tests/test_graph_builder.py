from src.model.graph_builder import GraphBuilder


def _dados():
    return {
        "processos": [
            {"processo_id": "F1", "nome": "Fonte", "tipo": "fonte"},
            {"processo_id": "A1", "nome": "Processo", "tipo": "processo"},
            {"processo_id": "P1", "nome": "Produto", "tipo": "produto_final"},
        ],
        "fluxos": [
            {"origem": "F1", "destino": "A1", "quantidade": 100, "unidade": "J"},
            {"origem": "A1", "destino": "P1", "quantidade": 1, "unidade": "J"},
        ],
    }


def test_construir_grafo_simples():
    grafo = GraphBuilder().construir_grafo(_dados(), {"F1": 48000})
    assert grafo.has_node("P1")


def test_obter_fontes_correto():
    builder = GraphBuilder()
    builder.construir_grafo(_dados(), {"F1": 48000})
    assert "F1" in builder.obter_fontes()


def test_obter_produtos_correto():
    builder = GraphBuilder()
    builder.construir_grafo(_dados(), {"F1": 48000})
    assert "P1" in builder.obter_produtos()


def test_normaliza_fracoes_de_saida():
    dados = {
        "processos": [
            {"processo_id": "F1", "nome": "Fonte", "tipo": "fonte"},
            {"processo_id": "A1", "nome": "A", "tipo": "processo"},
            {"processo_id": "B1", "nome": "B", "tipo": "processo"},
        ],
        "fluxos": [
            {"origem": "F1", "destino": "A1", "quantidade": 7, "unidade": "J"},
            {"origem": "F1", "destino": "B1", "quantidade": 3, "unidade": "J"},
        ],
    }
    grafo = GraphBuilder().construir_grafo(dados, {"F1": 48000})
    assert grafo.get_edge_data("F1", "A1")["fracao"] == 0.7
    assert grafo.get_edge_data("F1", "B1")["fracao"] == 0.3
