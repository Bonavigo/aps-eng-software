# 02 - Rede Solar e Biomassa

## Objetivo do teste

Testar a acumulação de emergia a partir de duas fontes distintas que alimentam um mesmo processo intermediário. O cenário também verifica a soma das contribuições percentuais em um único produto.

## Descrição da rede

- `F1` representa a Radiação Solar.
- `F2` representa a Água da Chuva.
- `P1` representa o Processo Fotossintético, que converte os insumos em biomassa.
- `PD1` representa a Biomassa Vegetal, produto final do sistema.

## Fontes e seus UEVs

- `F1` (Radiacao Solar): `uev = 1`
- `F2` (Agua da Chuva): `uev = 18199`
- Justificativa: a radiação solar é a referência base, e a chuva tem maior intensidade de emergia conforme os valores sugeridos no prompt.

## Resultado esperado

- Emergia total aproximada:
  - `F1`: `5.000.000 sej`
  - `F2`: `14.559.200 sej`
  - Total: `19.559.200 sej`
- Contribuição esperada:
  - `F1`: cerca de `25,56%`
  - `F2`: cerca de `74,44%`
- As contribuições devem somar aproximadamente `100%`.

## Como usar

1. Abra o programa SCALE - Emergy APS.
2. Selecione este diretório como espaço de trabalho.
3. Carregue `rede.csv` e `uevs.json`.
4. Execute o cálculo e confirme a distribuição entre as duas fontes.
