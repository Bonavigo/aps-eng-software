"""Janela de tutorial."""

from __future__ import annotations

import textwrap

import customtkinter as ctk


TEXTO_TUTORIAL = textwrap.dedent(
    """
    EmerCalc
    Sistema de Cálculo de Emergia para Redes LCI
    ------------------------------------------------------------

    O QUE É EMERGIA?

    Emergia é uma medida da energia total - direta e indireta - necessária para
    produzir um produto ou serviço, expressa em uma unidade padrão chamada sej
    (joules equivalentes solares). É usada em análises ambientais para comparar
    processos produtivos em termos de seu custo energético real para a natureza.

    ------------------------------------------------------------

    COMO USAR O PROGRAMA

    Passo 1 - Selecione o Espaço de Trabalho
    • Clique em "Navegar" no topo da tela.
    • Escolha a pasta onde estão os arquivos de entrada.
    • Os arquivos da pasta aparecerão listados na lateral esquerda.
    • Clique em um arquivo CSV para preenchê-lo automaticamente no campo
      "Arquivo de Rede".
    • Clique em um arquivo JSON para preenchê-lo automaticamente no campo
      "Arquivo de UEVs".

    Passo 2 - Verifique os Campos de Entrada
    • Confirme que os campos "Arquivo de Rede (CSV)" e "Arquivo de UEVs (JSON)"
      estão preenchidos corretamente com os caminhos dos seus arquivos.
    • Ajuste o Limiar de Propagação se necessário (veja abaixo).

    Passo 3 - Inicie o Cálculo
    • Clique em "Iniciar Cálculo".
    • Aguarde o progresso ser exibido na barra inferior.
    • Ao concluir, a janela de resultados será aberta automaticamente.

    Passo 4 - Exporte os Resultados
    • Use os botões "Exportar CSV", "Exportar PDF" ou "Exportar Grafo (PNG)"
      para salvar os resultados após o cálculo.

    ------------------------------------------------------------

    DESCRIÇÃO DE CADA CAMPO

    ESPAÇO DE TRABALHO
      Pasta no seu computador onde estão os arquivos de entrada.
      O programa lista os arquivos dessa pasta para facilitar a seleção.
      Não é obrigatório usar esta funcionalidade - você pode inserir os
      caminhos manualmente nos campos abaixo.

    ARQUIVO DE REDE (CSV)
      Arquivo de texto no formato CSV que descreve a rede de processos e fluxos
      da análise de ciclo de vida (LCI). Este arquivo deve seguir a estrutura:

      • Deve conter ao menos dois blocos separados por uma linha em branco:
        - Bloco 1: lista de processos
        - Bloco 2: lista de fluxos entre processos
        - Bloco 3 (opcional): valores UEV por processo

      • O bloco de processos deve ter as colunas:
        - processo_id (ou id): identificador único do processo
        - nome: nome legível do processo
        - tipo: tipo do processo (ex.: "fonte", "intermediario", "produto")

      • O bloco de fluxos deve ter as colunas:
        - origem: id do processo de origem
        - destino: id do processo de destino
        - quantidade: valor numérico positivo do fluxo
        - unidade: unidade de medida (ex.: MJ, kg, m³)

      Exemplo de arquivo CSV válido:

        processo_id,nome,tipo
        F1,Solar,fonte
        P1,Bomba,intermediario
        PD1,Agua,produto

        (linha em branco)

        origem,destino,quantidade,unidade
        F1,P1,5000,MJ
        P1,PD1,1,m³

    ARQUIVO DE UEVs (JSON)
      Arquivo no formato JSON que define o Valor de Unidade de Emergia (UEV)
      de cada fonte. O UEV representa quantos sej estão contidos em uma
      unidade do fluxo daquela fonte.

      A estrutura obrigatória do arquivo é:

        {
          "fontes": [
            { "id": "F1", "uev": 48000 },
            { "id": "F2", "uev": 15000 }
          ]
        }

      • O campo "id" deve corresponder ao processo_id de uma fonte no CSV.
      • O campo "uev" deve ser um número positivo maior que zero.
      • Fontes sem UEV definido no JSON serão ignoradas no cálculo.

    LIMIAR DE PROPAGAÇÃO (Threshold)
      Valor numérico entre 0 e 1 que controla a profundidade do cálculo.
      O programa percorre caminhos na rede de processos multiplicando os
      pesos dos fluxos ao longo do caminho. Quando o produto acumulado
      cai abaixo deste limiar, o caminho é encerrado.

      • Valor padrão: 0.1
      • Valores menores -> cálculo mais completo, mais lento
      • Valores maiores -> cálculo mais rápido, pode ignorar caminhos longos
      • Para análises precisas, use valores entre 0.01 e 0.05.
      • Nunca use 0 - o cálculo nunca terminaria.

    ------------------------------------------------------------

    SOBRE OS RESULTADOS

    Após o cálculo, uma janela de resultados é exibida com:

    • Tabela de contribuições: mostra cada fonte, sua emergia total acumulada
      em sej e sua porcentagem de contribuição para o produto final.

    • Gráfico de barras: visualização das contribuições relativas de cada fonte.

    Exportações disponíveis:
      CSV   -> tabela de contribuições em formato de planilha
      PDF   -> relatório completo com tabela, gráfico e referências
      PNG   -> imagem do grafo de processos com layout de força

    ------------------------------------------------------------

    ERROS COMUNS

    "Caminho vazio" ou "arquivo não encontrado"
      -> Verifique se os campos estão preenchidos e se os arquivos existem.

    "CSV sem seções suficientes"
      -> O arquivo CSV não possui os dois blocos obrigatórios separados por
         linha em branco (processos e fluxos).

    "Fluxo aponta para nó inexistente"
      -> Um dos valores de "origem" ou "destino" no bloco de fluxos não
         corresponde a nenhum processo_id no bloco de processos.

    "UEV ausente ou inválido"
      -> O JSON de UEVs tem um item sem campo "id", sem campo "uev",
         ou com uev igual a zero ou negativo.

    "Nenhum resultado para exportar"
      -> O cálculo ainda não foi executado nesta sessão. Execute o cálculo
         antes de tentar exportar.

    ------------------------------------------------------------

    === FIM DO CONTEÚDO DO TUTORIAL ===
    """
).strip()


class TutorialWindow(ctk.CTkToplevel):
    """Janela com explicação do sistema."""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.title("Tutorial - EmerCalc")
        self.geometry("980x760")
        self.transient(master)
        self.after_idle(self._centralizar_janela)
        texto = ctk.CTkTextbox(self, wrap="word")
        texto.insert("end", TEXTO_TUTORIAL)
        texto.configure(state="disabled")
        texto.pack(fill="both", expand=True, padx=8, pady=8)

    def _centralizar_janela(self) -> None:
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        if self.master is not None:
            master_x = self.master.winfo_rootx()
            master_y = self.master.winfo_rooty()
            master_largura = self.master.winfo_width()
            master_altura = self.master.winfo_height()
            x = max(0, master_x + (master_largura - largura) // 2)
            y = max(0, master_y + (master_altura - altura) // 2)
        else:
            tela_largura = self.winfo_screenwidth()
            tela_altura = self.winfo_screenheight()
            x = max(0, (tela_largura - largura) // 2)
            y = max(0, (tela_altura - altura) // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
