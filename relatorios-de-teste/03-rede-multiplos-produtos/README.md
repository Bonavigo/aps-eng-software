# 03 - Rede com Múltiplos Produtos

## Objetivo do teste

Verificar se o programa calcula corretamente dois produtos finais em paralelo, sem misturar contribuições entre ramos independentes da rede.

## Descrição da rede

- `F1` representa o Gás Natural.
- `F2` representa a Energia Elétrica.
- `F3` representa a Água de Rio.
- `P1` representa o Reator de Combustão.
- `P2` representa o Sistema de Filtragem.
- `PD1` representa o Calor Industrial.
- `PD2` representa a Água Purificada.
- O ramo `P1 -> PD1` gera o produto térmico e o ramo `P2 -> PD2` gera o produto hídrico.

## Fontes e seus UEVs

- `F1` (Gas Natural): `uev = 48000`
- `F2` (Energia Eletrica): `uev = 160000`
- `F3` (Agua de Rio): `uev = 48000`
- Justificativa: valores alinhados com os exemplos de referência do prompt.

## Resultado esperado

- Cada produto deve receber contribuição apenas das fontes do seu ramo.
- `PD1` deve refletir a soma dos caminhos vindos de `F1` e `F2`.
- `PD2` deve refletir a soma dos caminhos vindos de `F3` e `F2`.
- O resultado deve manter as contribuições separadas por fonte no relatório.

## Como usar

1. Abra o programa SCALE - Emergy APS.
2. Selecione este diretório como espaço de trabalho.
3. Carregue `rede.csv` e `uevs.json`.
4. Execute o cálculo e compare os dois produtos exibidos na janela de resultados.
