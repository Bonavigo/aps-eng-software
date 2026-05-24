from pathlib import Path

import pytest

from src.model.lci_manager import LCIError, LCIManager


def test_carregar_csv_valido():
    dados = LCIManager().carregar_csv(str(Path("tests/fixtures/rede_teste.csv")))
    assert len(dados["processos"]) == 3


def test_carregar_csv_invalido_campos_faltando(tmp_path):
    arquivo = tmp_path / "ruim.csv"
    arquivo.write_text("processo_id,nome,tipo\nA,Processo,processo\n\norigem,destino,quantidade,unidade\nA,B,,J\n", encoding="utf-8")
    with pytest.raises(LCIError):
        LCIManager().carregar_csv(str(arquivo))


def test_carregar_uevs_valido():
    uevs = LCIManager().carregar_uevs(str(Path("tests/fixtures/uevs_teste.json")))
    assert uevs["F1"] == 48000


def test_validar_dados_com_fluxo_para_no_inexistente():
    with pytest.raises(LCIError):
        LCIManager().validar_dados(
            {
                "processos": [{"processo_id": "A"}],
                "fluxos": [{"origem": "A", "destino": "B", "quantidade": 1, "unidade": "J"}],
            }
        )

