# Cenários de teste - EmerCalc

Arquivos de exemplo para testar importação, construção do grafo e cálculo de emergia.

## Formatos

- CSV: deve ter dois blocos separados por uma linha em branco.
- Bloco 1: processos, com `processo_id`, `nome` e `tipo`.
- Bloco 2: fluxos, com `origem`, `destino`, `quantidade` e `unidade`.
- JSON: deve conter a chave `fontes` com objetos no formato `{ "id": "...", "uev": ... }`.

## Arquivos Incluídos

- `exemplos/exemplo_rede_simples.csv`
- `exemplos/exemplo_rede_intermediaria.csv`
- `exemplos/exemplo_uevs.json`

## Cenários de Validação

Os cenários completos usados para teste manual ficam em `relatorios-de-teste/` na raiz do projeto.
Eles seguem a mesma convenção de CSV e JSON dos exemplos desta pasta.

## Observações

- Os nomes de processo devem ser consistentes entre o CSV e o JSON.
- O programa ignora fontes sem UEV válido no JSON.
- Quantidades nos fluxos devem ser positivas.
