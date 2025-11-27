from IPython.display import display # biblioteca para exibir DataFrames 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, norm
import math # biblioteca para funções matemáticas
import os # biblioteca para manipulação de caminhos e pastas

def run_analysis():
    """
    Executa a análise completa dos dados de Síndrome Gripal em SP (2022 e 2024),
    de forma semelhante ao script de COVID, mas adaptado para:
      - Idade
      - Sintomas
      - Evolução do caso
    """
    # Perguntas a serem respondidas:
    # 1. Qual a distribuição de idade dos casos notificados em 2022 e 2024?
    # 2. Quais os sintomas mais comuns em cada ano?
    # 3. Qual a taxa de evolução para casos graves (internação, óbito) em cada ano?
    # 4. Há diferenças estatísticas significativas entre os anos para idade, sintomas e evolução?
    # 5. Visualizações gráficas para comparar os anos.
    # --- FIM DAS PERGUNTAS ---
    
    #  1 ** --- CONFIGURAÇÕES INICIAIS ---
    dados = "dados"          # pasta onde estão os CSV
    output = "resultados"   # pasta onde os gráficos serão salvos
    os.makedirs(output, exist_ok=True) # cria a pasta resultados, se não existir ainda.

    # Nomes dos arquivos (dentro da pasta 'dados')
    
    path_2022 = os.path.join(dados, "Notificações de Síndrome Gripal - 2022_MAIOR.csv")
    path_2024 = os.path.join(dados, "Notificações de Síndrome Gripal - 2024_MAIOR.csv")

    try: #  ler os aruqivos CSV e caso de erro, gera uma mensagem erro. Vou ler só 5000 linhas para teste(nrows).
        df_amostra_2022 = pd.read_csv(path_2022, sep=";", encoding="latin1",engine="python", on_bad_lines="skip", nrows=5000)
        df_amostra_2024 = pd.read_csv(path_2024, sep=";", encoding="latin1",engine="python", on_bad_lines="skip", nrows=5000)
    except FileNotFoundError as e:
        print(f"Erro ao carregar os arquivos: {e}")
        return
    
    print("Carregamento dos dados concluído.")
    
    # Exibir linhas para conferência
    print("Amostra dos dados 2022:")
    print(df_amostra_2022, "\n")
    print("Amostra dos dados 2024:")
    print(df_amostra_2024, "\n")

    
    # Exibir informações básicas dos DataFrames
    print("Informações do DataFrame 2022:")
    print(df_amostra_2022.info(), "\n")
    print("Informações do DataFrame 2024:")
    print(df_amostra_2024.info(), "\n")
    
    
    
    
    # 2 ** --- TRATAMENTO DE BASES ---
    def preparar_ano(df, ano):
        
        df = df.copy() # cria uma cópia para evitar modificar o original
        df.columns = (
            df.columns # normaliza nomes de colunas para cada DataFrame: minúsculo, sem acento, sem espaços
            .str.strip() # remove espaços em branco nas extremidades
            .str.lower() # converte para minúsculo
            .str.normalize("NFKD") # normaliza para decompor caracteres acentuados
            .str.encode("ascii", "ignore") # remove caracteres não ASCII, por exemplo acentos serão ignorados
            .str.decode("ascii") # decodifica de volta para string, por exemplo 'ã' vira 'a'
        )
        
        df["ano"] = ano # adiciona coluna com o ano correspondente, logo, 2022 ou 2024
        return df # retorna o DataFrame modificado

    #converter idade para int64
    df_amostra_2022['idade'] = pd.to_numeric(df_amostra_2022['idade'], errors='coerce').astype('Int64')
    df_amostra_2024['idade'] = pd.to_numeric(df_amostra_2024['idade'], errors='coerce').astype('Int64')
    
    # ver como ficaram as coluna 
    print("Colunas do DataFrame 2022 após normalização:")
    print(df_amostra_2022.info(), "\n")
    print("Colunas do DataFrame 2024 após normalização:")
    print(df_amostra_2024.info(), "\n")
    
    # aqui corrigimos: 2022 e 2024
    df_amostra_2022 = preparar_ano(df_amostra_2022, 2022)
    df_amostra_2024 = preparar_ano(df_amostra_2024, 2024)
    
    #Ver como ficaram as colunas
    
    print("Colunas do DataFrame 2022 após normalização:")
    print(df_amostra_2022.info(), "\n")
    print("Colunas do DataFrame 2024 após normalização:")
    print(df_amostra_2024.info(), "\n")
        
    # Unificar as bases
    df_unificado = pd.concat([df_amostra_2022, df_amostra_2024], ignore_index=True) 
    
    # Exibir as primeiras linhas do DataFrame unificado para conferência
    print("Amostra dos dados unificados (2022 e 2024):")
    display(df_unificado, "\n")


    # Agora analisar variáveis de interesse: idade, sintomas, evolução do caso
    # vamos criar UM DATAFRAME só com as colunas de interesse para facilitar a análise
    colunas_interesse = [
        "idade",  # idade do paciente
        "sintomas",  # sintomas reportados (ex: febre, tosse, dor de garganta)
        "evolucaocaso",  # evolução do caso (ex: cura, internação, óbito)
        "ano"
    ]
    
    # Criar DataFrame só com colunas de interesse
    df_analise = df_unificado[colunas_interesse].copy()
    
    print("Amostra dos dados para análise (Com as colunas de interresse):")
    display(df_analise, "\n")
        
    # 3 ** -- Estatística descritiva --
    
    # Estatísticas descritivas para idade por ano
    estatisticas_idade = df_analise.groupby("ano")["idade"].describe()
    print("Estatísticas descritivas para idade por ano:")
    display(estatisticas_idade, "\n")
    
    # Estatísticas descritivas para sintomas por ano, mostrando separado para cada ano ( 4 mais comuns).
    sintomas_mais_comuns = (
        df_analise
        .groupby(["ano", "sintomas"])
        .size()
        .reset_index(name="contagem")
        .sort_values(by=["ano", "contagem"], ascending=[True, False])
        .groupby("ano")
        .head(4)
    )
    print("Sintomas mais comuns por ano:")
    display(sintomas_mais_comuns, "\n")
    
    # Estatísticas descritivas para evolução do caso por ano
    evolucao_caso = (
        df_analise
        .groupby(["ano", "evolucaocaso"])
        .size()
        .reset_index(name="contagem")
        .sort_values(by=["ano", "contagem"], ascending=[True, False])
    )
    print("Evolução do caso por ano:")
    display(evolucao_caso, "\n")
    
    
    
    # # 4 ** -- Probabilidade --
    
    # # 5 ** -- Inferencia estatística --
    
    
        
if __name__ == "__main__":
    run_analysis()       

