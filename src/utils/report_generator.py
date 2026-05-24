"""Geração de relatórios."""

from __future__ import annotations

import csv
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None


class ReportGenerator:
    """Exporta resultados em diferentes formatos."""

    def exportar_csv(self, resultados: dict[str, Any], caminho: str) -> None:
        """Escreve um CSV simples com as contribuições."""
        with Path(caminho).open("w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["Processo", "Emergia (sej)", "% Contribuição"])
            for processo, dados in resultados.get("contribuicoes", {}).items():
                writer.writerow([processo, dados["emergia"], dados["percentual"]])

    def exportar_pdf(self, resultados: dict[str, Any], caminho: str) -> None:
        """Gera um PDF com tabela, gráfico e sumário."""
        doc = SimpleDocTemplate(caminho, pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Relatório de Emergia", styles["Title"]),
            Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles["Normal"]),
            Spacer(1, 12),
        ]
        tabela = [["Processo", "Emergia (sej)", "% Contribuição"]]
        for processo, dados in resultados.get("contribuicoes", {}).items():
            tabela.append([processo, f"{dados['emergia']:.2f}", f"{dados['percentual']:.2f}"])
        table = Table(tabela, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )
        story.extend([table, Spacer(1, 12), self._imagem_contribuicao(resultados)])
        story.extend(
            [
                Spacer(1, 12),
                Paragraph("Referências: Odum (1996); Marvuglia et al. (2013).", styles["Normal"]),
            ]
        )
        doc.build(story)

    def exportar_grafo_png(self, grafo: Any, caminho: str) -> None:
        """Exporta o grafo de processos como PNG."""
        if grafo is None:
            raise ValueError("Grafo ausente para exportação PNG.")
        fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
        pos = nx.spring_layout(grafo, seed=42) if nx else None
        if nx:
            cores = []
            for no, attrs in grafo.nodes(data=True):
                tipo = attrs.get("tipo", "processo")
                cores.append({"fonte": "#2e7d32", "produto_final": "#c62828"}.get(tipo, "#1565c0"))
            nx.draw(grafo, pos, ax=ax, with_labels=True, node_color=cores, node_size=1200, font_size=8, arrows=True)
        fig.savefig(caminho, dpi=150)
        plt.close(fig)

    def _imagem_contribuicao(self, resultados: dict[str, Any]) -> Image:
        """Cria uma imagem embutida do gráfico de contribuição."""
        nomes = list(resultados.get("contribuicoes", {}).keys())
        valores = [dados["percentual"] for dados in resultados.get("contribuicoes", {}).values()]
        fig, ax = plt.subplots(figsize=(6.5, 3))
        ax.bar(nomes, valores, color="#1565c0")
        ax.set_ylabel("% contribuição")
        ax.set_ylim(0, max(valores + [100]) if valores else 100)
        ax.tick_params(axis="x", labelrotation=30)
        plt.tight_layout()
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=150)
        plt.close(fig)
        buffer.seek(0)
        return Image(buffer, width=400, height=180)
