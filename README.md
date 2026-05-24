# SCALE - Emergy APS

Aplicação desktop em Python para importação de redes LCI, cálculo de emergia, visualização dos resultados e exportação de relatórios em CSV, PDF e PNG.

## Visão Geral

- Importa arquivos CSV com processos e fluxos.
- Importa arquivos JSON com UEVs das fontes.
- Constrói o grafo da rede LCI.
- Calcula a emergia por fonte e o total do produto.
- Exibe os resultados em interface gráfica.
- Exporta relatórios e imagens do grafo.
- Inclui cenários de teste completos em `relatorios-de-teste/`.

## Requisitos

- Python 3.13
- `customtkinter`
- `matplotlib`
- `reportlab`
- `networkx` opcional, com fallback interno quando indisponível

## Como Rodar

Use o Python instalado na conta do usuário da máquina:

```powershell
& "C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python313\python.exe" main.py
```

Se preferir, execute diretamente no ambiente ativo:

```bash
python main.py
```

## Interface

A aplicação usa `customtkinter` nas janelas da interface. O visual principal
é carregado em tema escuro e a navegação entre workspace, cálculo, tutorial e
resultados fica na própria GUI.

## Testes

Execute a suíte automatizada com:

```bash
pytest tests/
```

Para validar todo o fluxo de cálculo com os cenários de exemplo, você também pode usar os arquivos em `data/exemplos/` e `relatorios-de-teste/`.

## Como Usar

1. Abra a aplicação.
2. Selecione um workspace com arquivos de entrada.
3. Preencha o arquivo CSV da rede e o JSON de UEVs.
4. Ajuste o limiar de propagação, se necessário.
5. Clique em `Iniciar Cálculo`.
6. Veja a janela de resultados e exporte o que precisar.

## Dados de Exemplo

- `relatorios-de-teste/01-rede-simples/`
- `relatorios-de-teste/02-rede-solar-biomassa/`
- `relatorios-de-teste/03-rede-multiplos-produtos/`
- `relatorios-de-teste/04-rede-grande/`
- `relatorios-de-teste/05-rede-com-convergencia/`

## Cenários de Validação

Os cenários completos de teste ficam em `relatorios-de-teste/`:

- `01-rede-simples`
- `02-rede-solar-biomassa`
- `03-rede-multiplos-produtos`
- `04-rede-grande`
- `05-rede-com-convergencia`

Cada pasta contém:

- `rede.csv`
- `uevs.json`
- `README.md`

## Estrutura do Projeto

- `src/model`: importação, grafo e cálculo
- `src/view`: janelas da interface
- `src/controller`: coordenação do fluxo
- `src/utils`: exportação de resultados
- `data`: exemplos e documentação dos dados
- `relatorios-de-teste`: cenários de teste manuais
- `tests`: testes automatizados
- `data`: arquivos de exemplo e documentação dos dados
- `relatorios-de-teste`: cenários completos para validação manual

## Fluxo da Aplicação

1. O CSV é lido e validado.
2. O JSON de UEVs é carregado.
3. O grafo é construído com os nós e fluxos.
4. O cálculo percorre os caminhos válidos entre fontes e produtos.
5. O resultado é exibido na interface.
6. O usuário pode exportar CSV, PDF ou PNG.

## Observações Sobre o Cálculo

- Fontes e produtos são identificados pelos atributos do grafo.
- As arestas são normalizadas por frações de saída.
- Caminhos repetidos e ciclos são tratados durante a exploração.
- O resultado final inclui emergia total, contribuição por fonte e métricas de perda.

## Referências

- ODUM, Howard T. *Environmental Accounting: Emergy and Environmental Decision Making*. 1996.
- MARVUGLIA, Antonino et al. *SCALE: Software for CALculating Emergy based on Life Cycle Inventories*. 2013.
- ARBAULT, Damien et al. *Emergy evaluation using the calculation software SCALE*. 2014.

## Observações Sobre o Cálculo

- O programa identifica fontes e produtos pelos atributos de tipo do grafo.
- As arestas recebem frações normalizadas a partir da soma dos fluxos de saída.
- Caminhos são explorados com controle de ciclos e limiar de propagação.
- O resultado final mostra emergia total, contribuição por fonte, caminho explorado e métricas de perda.

## Integrantes

- Bruno Bonavigo
- Lucas Vergara
- Helen Silva
- Vitor Oliveira
