# 04 - Rede Grande

## Objetivo do teste

Exercitar a execução em uma rede mais complexa, com várias camadas de intermediários e dois produtos finais. O objetivo é validar desempenho, estabilidade e percurso de múltiplos caminhos.

## Descrição da rede

- `F1`, `F2`, `F3` e `F4` representam quatro fontes distintas.
- `P1`, `P2` e `P3` formam a camada de processamento primário.
- `P4`, `P5` e `P6` formam a camada de distribuição.
- `PD1` representa a Eletricidade Distribuida.
- `PD2` representa a Agua Pressurizada.
- Os fluxos convergem em `P6` e se desdobram em dois produtos finais.

## Fontes e seus UEVs

- `F1` (Energia Solar Direta): `uev = 1`
- `F2` (Energia Eolica): `uev = 1496`
- `F3` (Agua de Rio): `uev = 48000`
- `F4` (Gas Natural): `uev = 48000`
- Justificativa: conjunto diversificado de referências para testar a agregação de emergia em uma rede maior.

## Resultado esperado

- O cálculo deve retornar contribuições distribuídas entre quatro fontes.
- A janela de resultados deve listar ambos os produtos sem travamentos.
- A emergia total deve refletir a soma dos caminhos válidos até `PD1` e `PD2`.

## Como usar

1. Abra o programa EmerCalc.
2. Selecione este diretório como espaço de trabalho.
3. Carregue `rede.csv` e `uevs.json`.
4. Execute o cálculo para validar a navegação em rede grande.
