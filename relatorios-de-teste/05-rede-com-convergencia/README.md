# 05 - Rede com Convergência

## Objetivo do teste

Exercitar o mecanismo de prevenção de dupla contagem em uma rede com convergência de caminhos. Duas fontes alimentam ramos diferentes que se encontram em um único intermediário antes do produto final.

## Descrição da rede

- `F1` representa a Energia Geotermica.
- `F2` representa a Energia Maremotriz.
- `P1` representa a Turbina Geotermica.
- `P2` representa a Turbina Maremotriz.
- `P3` representa o Conversor de Tensao, ponto de convergência dos ramos.
- `PD1` representa a Eletricidade de Baixo Impacto.

## Fontes e seus UEVs

- `F1` (Energia Geotermica): `uev = 34377`
- `F2` (Energia Maremotriz): `uev = 26000`
- Justificativa: valores positivos e distintos para observar a soma das contribuições sem duplicação do caminho convergente.

## Resultado esperado

- O programa deve contabilizar cada par fonte/produto apenas uma vez.
- As contribuições de `F1` e `F2` devem aparecer separadas na tabela final.
- O total deve refletir os caminhos válidos até `PD1`, sem dupla contagem.

## Como usar

1. Abra o programa EmerCalc.
2. Selecione este diretório como espaço de trabalho.
3. Carregue `rede.csv` e `uevs.json`.
4. Execute o cálculo e verifique a ausência de duplicações na saída.
