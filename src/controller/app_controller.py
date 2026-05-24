"""Controlador da aplicação."""

from __future__ import annotations

import json
import threading
from typing import Any, Callable

from src.agent.emergy_agent import EmergiaAgent
from src.model.lci_manager import LCIError
from src.utils.report_generator import ReportGenerator


class AppController:
    """Coordena cálculo, exportação e comunicação com a GUI."""

    def __init__(self) -> None:
        self.agent = EmergiaAgent()
        self.report = ReportGenerator()
        self.ultimos_resultados: dict[str, Any] | None = None
        self.ultima_entrada: dict[str, str] | None = None

    def iniciar_calculo(
        self,
        params: dict[str, Any],
        on_done: Callable[[dict[str, Any]], None] | None = None,
        *,
        on_status: Callable[[str], None] | None = None,
        on_error: Callable[[dict[str, str]], None] | None = None,
    ) -> threading.Thread:
        """Executa o cálculo em uma thread e reporta status/erros."""

        def tarefa() -> None:
            try:
                caminho_grafo = params["caminho_grafo"]
                caminho_uevs = params["caminho_uevs"]
                threshold = float(params.get("threshold", 0.1))

                self._emitir_status(on_status, "Carregando arquivos de entrada...")
                dados = self.agent.manager.carregar_csv(caminho_grafo)
                uevs = self.agent.manager.carregar_uevs(caminho_uevs)

                self._emitir_status(on_status, "Validando dados...")
                self.agent.manager.validar_dados(dados)
                self._validar_uevs(dados, uevs)

                self._emitir_status(on_status, "Construindo grafo de processos...")
                grafo = self.agent.builder.construir_grafo(dados, uevs)

                self._emitir_status(on_status, "Calculando emergia...")
                resultado = self.agent.calculator.calcular(
                    grafo,
                    threshold=threshold,
                    callback=params.get("callback"),
                )
                resultado["grafo"] = grafo

                self.ultimos_resultados = resultado
                self.ultima_entrada = {
                    "caminho_grafo": caminho_grafo,
                    "caminho_uevs": caminho_uevs,
                    "threshold": str(threshold),
                }
                self._emitir_status(on_status, "Cálculo concluído.")
                if on_done:
                    on_done(resultado)
            except Exception as exc:  # pragma: no cover - as falhas são validadas na UI
                self._emitir_erro(on_error, exc)

        thread = threading.Thread(target=tarefa, daemon=True)
        thread.start()
        return thread

    def exportar_resultados(self, tipo: str, caminho: str) -> None:
        if not self.ultimos_resultados:
            raise RuntimeError("Não há resultados para exportar.")
        if tipo == "csv":
            self.report.exportar_csv(self.ultimos_resultados, caminho)
        elif tipo == "pdf":
            self.report.exportar_pdf(self.ultimos_resultados, caminho)
        elif tipo == "png":
            self.report.exportar_grafo_png(self.ultimos_resultados.get("grafo"), caminho)
        else:
            raise ValueError(f"Tipo de exportação inválido: {tipo}")

    def _emitir_status(self, callback: Callable[[str], None] | None, mensagem: str) -> None:
        if callback:
            callback(mensagem)

    def _emitir_erro(self, callback: Callable[[dict[str, str]], None] | None, exc: Exception) -> None:
        if not callback:
            return
        callback(self._classificar_erro(exc))

    def _validar_uevs(self, dados: dict[str, Any], uevs: dict[str, float]) -> None:
        fontes = [
            str(processo.get("processo_id") or processo.get("id"))
            for processo in dados.get("processos", [])
            if str(processo.get("tipo", "")).strip().lower() == "fonte"
        ]
        faltantes = [fonte for fonte in fontes if float(uevs.get(fonte, 0.0) or 0.0) <= 0]
        if faltantes:
            lista = ", ".join(faltantes)
            raise LCIError(f"UEV ausente ou inválido para as fontes: {lista}.")

    def _classificar_erro(self, exc: Exception) -> dict[str, str]:
        mensagem = str(exc)
        mensagem_lower = mensagem.lower()

        if isinstance(exc, FileNotFoundError) or "não encontrado" in mensagem_lower or "caminho vazio" in mensagem_lower:
            return {
                "codigo": "2",
                "titulo": "Arquivo não encontrado",
                "mensagem": "Não foi possível localizar um dos arquivos informados.",
                "explicacao": mensagem,
                "solucao": "Verifique o caminho do CSV e do JSON, confirme se os arquivos existem e tente novamente.",
            }
        if "csv inválido" in mensagem_lower or "csv" in mensagem_lower and ("seção" in mensagem_lower or "fluxo inválido" in mensagem_lower or "nenhum processo encontrado" in mensagem_lower):
            return {
                "codigo": "3",
                "titulo": "CSV inválido",
                "mensagem": "O arquivo CSV informado não segue a estrutura esperada.",
                "explicacao": mensagem,
                "solucao": "Use um CSV com blocos de processos e fluxos separados por uma linha em branco.",
            }
        if isinstance(exc, json.JSONDecodeError) or ("json de uevs inválido" in mensagem_lower or ("json" in mensagem_lower and "uev" in mensagem_lower and "inválido" in mensagem_lower)):
            return {
                "codigo": "4",
                "titulo": "JSON inválido",
                "mensagem": "O arquivo JSON de UEVs não pôde ser processado.",
                "explicacao": mensagem,
                "solucao": "Confira a chave \"fontes\" e o formato {\"id\": \"...\", \"uev\": ...}.",
            }
        if "fluxo referencia nó inexistente" in mensagem_lower or "fluxo aponta para nó inexistente" in mensagem_lower:
            return {
                "codigo": "5",
                "titulo": "Referência inválida",
                "mensagem": "Existe um fluxo apontando para um nó que não está definido no CSV.",
                "explicacao": mensagem,
                "solucao": "Corrija os valores de origem e destino no bloco de fluxos do CSV.",
            }
        if "uev ausente ou inválido" in mensagem_lower or "uev inválido" in mensagem_lower:
            return {
                "codigo": "6",
                "titulo": "UEV ausente ou inválido",
                "mensagem": "Uma fonte da rede não possui UEV válido.",
                "explicacao": mensagem,
                "solucao": "Inclua um UEV positivo no JSON para todas as fontes usadas na rede.",
            }
        if "threshold" in mensagem_lower or "limiar" in mensagem_lower:
            return {
                "codigo": "7",
                "titulo": "Limiar inválido",
                "mensagem": "O limiar informado não é válido para o cálculo.",
                "explicacao": mensagem,
                "solucao": "Informe um valor numérico entre 0 e 1.",
            }
        return {
            "codigo": "9",
            "titulo": "Falha inesperada",
            "mensagem": "O cálculo encontrou um erro inesperado.",
            "explicacao": mensagem,
            "solucao": "Revise os arquivos de entrada e tente novamente. Se o problema persistir, verifique o relatório gerado pela aplicação.",
        }
