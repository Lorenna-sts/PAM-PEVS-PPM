# Processamento de Dados do IBGE (PAM, PPM, PEVS)

Este notebook Jupyter foi desenvolvido para automatizar a extração, transformação e formatação de dados de pesquisas agropecuárias do IBGE, especificamente:

*   **PAM**: Produção Agrícola Municipal
*   **PPM**: Pesquisa da Pecuária Municipal
*   **PEVS**: Produção da Extração Vegetal e da Silvicultura

O objetivo final é preparar e estruturar esses dados para serem integrados ao Banco de Dados Estatísticos (BDE) de Goiás, focando nos municípios do estado.

## ⚙️ Funcionalidades

1.  **Extração de Dados**: Conecta-se à API SIDRA do IBGE para buscar dados de tabelas específicas relacionadas às pesquisas selecionadas.
2.  **Transformação**: Processa os dados brutos da API, convertendo-os para um formato tabular (DataFrame do Pandas) e criando um código de fonte (`codFonte`) para junção.
3.  **Enriquecimento**: Combina os dados extraídos com metadados locais, como a lista de municípios de Goiás e um mapeamento de variáveis (de-para entre o `codFonte` e o código da variável no BDE).
4.  **Formatação**: Ajusta os dados para o layout final exigido pelo BDE, incluindo a formatação de valores numéricos e a renomeação de colunas.
5.  **Exportação**: Salva o resultado final em um arquivo CSV pronto para importação.

## 📋 Pré-requisitos

Para executar este notebook, você precisará de:

*   Python 3
*   As seguintes bibliotecas Python, que podem ser instaladas via `pip`:
    *   `pandas`
    *   `requests`
    *   `ipywidgets`
    *   `openpyxl` (necessário para `pd.read_excel`)
    *   `pybdedata` (a primeira célula do notebook já inclui o comando de instalação)

## 🚀 Como Usar

### 1. Configuração

Antes de executar o notebook, verifique as seguintes configurações:

*   **Seleção da Pesquisa**: Na célula `[4]` (no arquivo original, agora `[5]`), defina a variável `pesquisa` para a sigla da pesquisa desejada. As opções pré-configuradas são:
    *   `'PEVS'`
    *   `'PPM'`
    *   `'PAM'`

    ```python
    # Célula de exemplo
    pesquisa = 'PEVS' # Altere aqui para 'PPM' ou 'PAM'
    dados = getSource(pesquisa)
    ```

*   **Caminho dos Arquivos**: Certifique-se de que os caminhos para os arquivos externos (rede ou locais) estão corretos e acessíveis:
    *   **Mapeamento de Variáveis**: Na célula `[6]`, o caminho para `tb_bde-cod-ibge.xlsx` deve estar correto.
        ```python
        # Célula [6]
        src = r'Z:/GEDE/BDE - Banco de Dados/tb_bde-cod-ibge.xlsx'
        ```
    *   **Exportação do CSV**: Na última célula (`[17]`), o caminho de destino para o arquivo CSV final deve ser válido.
        ```python
        # Célula [17]
        db.to_csv('Z:\\GEDE\\BDE - Banco de Dados\\...\\dados_exportados.csv', ...)
        ```

### 2. Execução

Execute as células do notebook em sequência. O fluxo principal é:

1.  **`getSource(pesquisa)`**: Extrai os dados da API do IBGE para a pesquisa selecionada.
2.  **Carregamento de Metadados**: Carrega o arquivo Excel de mapeamento de variáveis (`dfvar`) e a lista de municípios de Goiás (`locations`).
3.  **Merge e Transformação**: Une os DataFrames `dados`, `locations` e `dfvar` para criar a tabela final (`datamerge`).
4.  **Formatação e Exportação**: Formata a tabela `datamerge` para o layout de importação e a salva como CSV.

## 📂 Estrutura do Código

*   **Células `[1]`-`[4]`**: Importação de bibliotecas, definição de URLs e das funções `formatUnitMilhar` e `getSource`. A função `getSource` é o núcleo da extração, configurando e executando as chamadas à API SIDRA.
*   **Célula `[5]`**: Executa a extração de dados para a pesquisa definida na variável `pesquisa`.
*   **Células `[6]`-`[8]`**: Carregam dados auxiliares: o mapeamento de variáveis do BDE a partir de um arquivo Excel e a lista de municípios de Goiás via biblioteca `pybdedata`.
*   **Células `[9]`-`[11]`**: Realizam a junção (`merge`) dos dados extraídos do IBGE com os dados de municípios e de mapeamento de variáveis para enriquecer o dataset.
*   **Células `[12]`-`[16]`**: Preparam o DataFrame final (`db`) para exportação, renomeando colunas e selecionando os campos necessários para o layout de importação do BDE.
*   **Célula `[17]`**: Exporta o DataFrame final para um arquivo `.csv`.