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

