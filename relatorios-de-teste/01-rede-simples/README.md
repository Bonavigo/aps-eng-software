# 01 - Rede Simples

## Objetivo do teste

Validar o caso mínimo do programa, com uma única fonte ligada diretamente a um único produto. Este cenário verifica se o cálculo básico de emergia funciona sem intermediários.

## Descrição da rede

- `F1` representa a Energia Solar, a fonte primária da rede.
- `PD1` representa a Biomassa Primaria, produto final do sistema.
- O fluxo `F1 -> PD1` transfere `1.000.000 J` diretamente para o produto.

## Fontes e seus UEVs

- `F1` (Energia Solar): `uev = 1`
- Justificativa: energia solar direta é a referência mínima de emergia.

## Resultado esperado

- Emergia total aproximada: `1.000.000 sej`
- Contribuição esperada:
  - `F1`: `100%`
- Como há apenas uma fonte, todo o resultado deve ser atribuído a `F1`.

## Como usar

1. Abra o programa EmerCalc.
2. Selecione este diretório como espaço de trabalho.
3. Carregue `rede.csv` e `uevs.json`.
4. Clique em `Iniciar Cálculo` para executar o teste.
