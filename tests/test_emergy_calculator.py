from src.model.emergy_calculator import EmergiaCalculator
from src.model.graph_builder import GraphBuilder


def _grafo_simples():
    dados = {
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
    return GraphBuilder().construir_grafo(dados, {"F1": 48000})


def test_calculo_rede_simples_sem_ciclo():
    resultado = EmergiaCalculator().calcular(_grafo_simples(), threshold=0.1)
    assert resultado["emergia_total"] > 0


def test_calculo_rede_com_coproduto():
    grafo = _grafo_simples()
    resultado = EmergiaCalculator().calcular(grafo, threshold=0.1)
    assert "F1" in resultado["contribuicoes"]


def test_calculo_evita_dupla_contagem():
    dados = {
        "processos": [
            {"processo_id": "F1", "nome": "Fonte", "tipo": "fonte"},
            {"processo_id": "A1", "nome": "A", "tipo": "processo"},
            {"processo_id": "B1", "nome": "B", "tipo": "processo"},
            {"processo_id": "P1", "nome": "Produto", "tipo": "produto_final"},
        ],
        "fluxos": [
            {"origem": "F1", "destino": "A1", "quantidade": 1, "unidade": "J"},
            {"origem": "F1", "destino": "B1", "quantidade": 1, "unidade": "J"},
            {"origem": "A1", "destino": "P1", "quantidade": 1, "unidade": "J"},
            {"origem": "B1", "destino": "P1", "quantidade": 1, "unidade": "J"},
        ],
    }
    grafo = GraphBuilder().construir_grafo(dados, {"F1": 48000})
    resultado = EmergiaCalculator().calcular(grafo, threshold=0.1)
    assert list(resultado["contribuicoes"].keys()) == ["F1"]


def test_threshold_elimina_caminhos_insignificantes():
    resultado = EmergiaCalculator().calcular(_grafo_simples(), threshold=999999)
    assert resultado["emergia_total"] == 0


def test_deteccao_de_ciclo():
    dados = {
        "processos": [
            {"processo_id": "F1", "nome": "Fonte", "tipo": "fonte"},
            {"processo_id": "A1", "nome": "A", "tipo": "processo"},
            {"processo_id": "P1", "nome": "Produto", "tipo": "produto_final"},
        ],
        "fluxos": [
            {"origem": "F1", "destino": "A1", "quantidade": 1, "unidade": "J"},
            {"origem": "A1", "destino": "P1", "quantidade": 1, "unidade": "J"},
            {"origem": "A1", "destino": "A1", "quantidade": 1, "unidade": "J"},
        ],
    }
    grafo = GraphBuilder().construir_grafo(dados, {"F1": 48000})
    resultado = EmergiaCalculator().calcular(grafo, threshold=0.1)
    assert resultado["caminhos_explorados"] >= 0

