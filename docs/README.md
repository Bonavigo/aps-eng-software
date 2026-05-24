# Documentação técnica - EmerCalc

## Escopo
Sistema em Python para cálculo de emergia com importação de LCI, cálculo por backtracking e interface gráfica.

## Requisitos
- Funcionais: importação de dados, grafo, cálculo, relatórios, GUI e testes.
- Não funcionais: Python 3.10+, Tkinter, Git, pytest e modularização MVC.

## Estrutura
- `src/model`: LCI, grafo e cálculo
- `src/agent`: pipeline de coordenação
- `src/controller`: integração com a interface
- `src/view`: GUI principal e janelas auxiliares
- `src/utils`: exportação CSV, PDF e PNG

## Uso
1. Abrir a aplicação com `python main.py`.
2. Selecionar um workspace.
3. Informar o arquivo CSV do grafo e o JSON de UEVs.
4. Executar o cálculo.
5. Exportar os resultados em CSV, PDF ou PNG.

## Algoritmo
O cálculo percorre caminhos simples do grafo entre fontes e produtos, evita ciclos por conjunto de visitados e soma contribuições únicas por fonte.

## Testes
Estratégia orientada a TDD com foco em importação, construção do grafo e cálculo.

## Referências
- ODUM, Howard T. Environmental Accounting: Emergy and Environmental Decision Making. 1996.
- MARVUGLIA, Antonino et al. SCALE: Software for CALculating Emergy based on Life Cycle Inventories. 2013.
- ARBAULT, Damien et al. Emergy evaluation using the calculation software SCALE. 2014.
