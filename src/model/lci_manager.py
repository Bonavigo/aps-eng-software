"""Importação e validação de dados LCI.

Docstrings em português, seguindo o padrão Google Style.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


class LCIError(ValueError):
    """Erro de validação dos dados LCI."""


class LCIManager:
    """Gerencia carregamento e validação dos dados LCI."""

    def carregar_csv(self, caminho: str) -> dict[str, list[dict[str, Any]]]:
        """Lê um arquivo CSV com seções de processos, fluxos e UEVs."""
        texto = Path(caminho).read_text(encoding="utf-8-sig")
        blocos = [bloco.strip() for bloco in texto.split("\n\n") if bloco.strip()]
        if len(blocos) < 2:
            raise LCIError("CSV inválido: esperado ao menos seções de processos e fluxos.")

        def ler_bloco(bloco: str) -> list[dict[str, Any]]:
            linhas = [linha for linha in bloco.splitlines() if linha.strip()]
            leitor = csv.DictReader(linhas)
            return list(leitor)

        processos = ler_bloco(blocos[0])
        fluxos = ler_bloco(blocos[1])
        uevs = ler_bloco(blocos[2]) if len(blocos) > 2 else []
        dados = {"processos": processos, "fluxos": fluxos, "uevs": uevs}
        self.validar_dados(dados)
        return dados

    def carregar_uevs(self, caminho: str) -> dict[str, float]:
        """Lê UEVs a partir de um JSON."""
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
        fontes = dados.get("fontes", [])
        uevs: dict[str, float] = {}
        for fonte in fontes:
            fonte_id = fonte.get("id")
            uev = fonte.get("uev")
            if not fonte_id or uev is None:
                raise LCIError("JSON de UEVs inválido: campos obrigatórios ausentes.")
            uev = float(uev)
            if uev <= 0:
                raise LCIError(f"UEV inválido para {fonte_id}: deve ser positivo.")
            uevs[str(fonte_id)] = uev
        return uevs

    def validar_dados(self, dados: dict[str, list[dict[str, Any]]]) -> bool:
        """Valida integridade básica dos dados importados."""
        processos = dados.get("processos", [])
        fluxos = dados.get("fluxos", [])
        ids = {str(item.get("processo_id") or item.get("id")) for item in processos}
        ids.discard("None")
        if not ids:
            raise LCIError("Nenhum processo encontrado nos dados.")
        for fluxo in fluxos:
            origem = fluxo.get("origem")
            destino = fluxo.get("destino")
            quantidade = fluxo.get("quantidade")
            if not origem or not destino or quantidade in (None, ""):
                raise LCIError("Fluxo inválido: campos obrigatórios ausentes.")
            if origem not in ids or destino not in ids:
                raise LCIError(f"Fluxo referencia nó inexistente: {origem} -> {destino}.")
            if float(quantidade) <= 0:
                raise LCIError("Fluxo inválido: quantidade deve ser positiva.")
        return True

