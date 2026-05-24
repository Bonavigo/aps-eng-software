# Sistema de Cálculo de Emergia

Projeto da APS de Engenharia de Software para importação de LCI, cálculo de emergia, geração de relatórios e interface gráfica em `customtkinter`.

## Visão Geral

- Importa redes LCI em CSV e UEVs em JSON.
- Constrói o grafo de processos.
- Calcula emergia por fonte e por produto.
- Exporta resultados em CSV, PDF e PNG.
- Inclui cenários de teste em `relatorios-de-teste/`.

## Como rodar

Use o Python 3.13 instalado no seu usuário:

```powershell
& "C:\Users\bbona\AppData\Local\Programs\Python\Python313\python.exe" main.py
```

## Execução

```bash
python main.py
```

## Interface

A aplicação usa `customtkinter` nas janelas da interface. O visual principal
é carregado em tema escuro e a navegação entre workspace, cálculo, tutorial e
resultados fica na própria GUI.

## Testes

```bash
pytest tests/
```

## Dados de Exemplo

- `data/exemplos/exemplo_rede_simples.csv`
- `data/exemplos/exemplo_rede_intermediaria.csv`
- `data/exemplos/exemplo_uevs.json`
- `relatorios-de-teste/01-rede-simples/`
- `relatorios-de-teste/02-rede-solar-biomassa/`
- `relatorios-de-teste/03-rede-multiplos-produtos/`
- `relatorios-de-teste/04-rede-grande/`
- `relatorios-de-teste/05-rede-com-convergencia/`

Você pode selecionar esses arquivos diretamente na GUI depois de escolher um workspace.

## Estrutura

- `src/model`: importação, grafo e cálculo
- `src/view`: telas da aplicação
- `src/controller`: coordenação do fluxo
- `src/utils`: exportações
- `tests`: testes automatizados
- `data`: arquivos de exemplo e documentação dos dados
- `relatorios-de-teste`: cenários completos para validação manual

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

- `NOME_ALUNO_1`
- `NOME_ALUNO_2`
