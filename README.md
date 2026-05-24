# Sistema de Cálculo de Emergia

Projeto da APS de Engenharia de Software para importação de LCI, cálculo de emergia, geração de relatórios e interface gráfica em Tkinter.

## Como rodar

Use o Python 3.13 instalado no seu usuário:

```powershell
& "C:\Users\bbona\AppData\Local\Programs\Python\Python313\python.exe" main.py
```

## Execução

```bash
python main.py
```

## Testes

```bash
pytest tests/
```

## Dados de Exemplo

- `data/exemplos/exemplo_rede_simples.csv`
- `data/exemplos/exemplo_uevs.json`

Você pode selecionar esses arquivos diretamente na GUI depois de escolher um workspace.

## Estrutura

- `src/model`: importação, grafo e cálculo
- `src/view`: telas da aplicação
- `src/controller`: coordenação do fluxo
- `src/utils`: exportações
- `tests`: testes automatizados

## Referências

- ODUM, Howard T. *Environmental Accounting: Emergy and Environmental Decision Making*. 1996.
- MARVUGLIA, Antonino et al. *SCALE: Software for CALculating Emergy based on Life Cycle Inventories*. 2013.
- ARBAULT, Damien et al. *Emergy evaluation using the calculation software SCALE*. 2014.

## Integrantes

- `NOME_ALUNO_1`
- `NOME_ALUNO_2`
