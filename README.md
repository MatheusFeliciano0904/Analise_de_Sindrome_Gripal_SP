# 📊 Análise de Síndrome Gripal – SP (2023–2024)

Este repositório contém uma análise completa dos dados de **Síndrome Gripal no estado de São Paulo** para os anos de **2023 e 2024**.  
O projeto realiza limpeza, padronização, exploração estatística, testes de hipótese e geração de gráficos automáticos.

---

## 📁 Estrutura do Repositório

📦 Analise_de_Sindrome_Gripal_SP
│
├── dados/
│ ├── Notificações de Síndrome Gripal_SP_2023.csv
│ └── Notificações de Síndrome Gripal_SP_2024.csv
│
├── resultados/
│ ├── histograma_idade.png
│ ├── boxplot_idade_ano.png
│ ├── grafico_sexo_por_ano.png
│
├── analise_sindrome_gripal.py
├── README.md
├── Instruções.pdf
├── .gitignore
└── .gitattributes


---

## 🧠 O que o script faz?

O arquivo **`analise_sindrome_gripal.py`** contém a função `run_analysis()`, que executa toda a análise automaticamente em **6 etapas principais**:

1. **Carregamento dos dados**  
   - Lê os arquivos CSV de 2023 e 2024 a partir da pasta `dados/`.  
   - Usa `sep=";"`, codificação `latin1` e ignora linhas problemáticas (`on_bad_lines="skip"`).

2. **Padronização e unificação**  
   - Normaliza os nomes de colunas (minúsculo, sem acentos, sem espaços especiais).  
   - Adiciona a coluna `ano` (2023 ou 2024).  
   - Une as duas bases em um único DataFrame `df_final`.

3. **Preparação das variáveis**  
   - Converte a coluna `idade` para numérico.  
   - Converte `datanotificacao` para `datetime` (se existir).  
   - Cria a coluna `num_sintomas`, contando quantos sintomas foram registrados na coluna `sintomas`.

4. **Estatística descritiva**  
   - Calcula estatísticas descritivas gerais para `idade` e `num_sintomas`.  
   - Calcula estatísticas descritivas de idade **por ano** (2023 vs 2024).

5. **Geração de gráficos** (salvos na pasta `resultados/`)  
   - `histograma_idade.png`: histograma da idade de todos os casos, com curva KDE.  
   - `boxplot_idade_ano.png`: boxplot comparando a distribuição de idade entre 2023 e 2024.  
   - `grafico_sexo_por_ano.png`: gráfico de barras mostrando a distribuição de casos por sexo em cada ano.

6. **Testes de hipótese e probabilidades**  
   - **Teste t de Student** (independente) para comparar a idade média entre 2023 e 2024.  
   - **Teste de proporção** para um sintoma específico (por padrão, `Tosse`), comparando sua frequência entre 2023 e 2024.  
   - Cálculo da probabilidade de um caso ter **idade ≥ 35 anos**.  
   - Cálculo da probabilidade de um caso ter **“muitos sintomas”** (acima do percentil 75 de `num_sintomas`).

---

## 🛠️ Tecnologias Utilizadas

- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- SciPy (`ttest_ind`, `norm`)  
- Math e OS (manipulação numérica e de arquivos)

---

## 📈 Principais Insights (em potencial)

- Verificação se há ou não **diferença significativa** na idade média entre 2023 e 2024.  
- Identificação de **predomínio por sexo** nas notificações anuais.  
- Avaliação da **frequência de sintomas** ao longo dos anos (ex.: Tosse).  
- Estimativa de probabilidades associadas à idade e ao número de sintomas.

---

## ▶️ Como Executar

1. Certifique-se de ter os arquivos CSV dentro da pasta `dados/` com os nomes:
   - `Notificações de Síndrome Gripal_SP_2023.csv`
   - `Notificações de Síndrome Gripal_SP_2024.csv`

2. Instale as dependências (via `pip`, por exemplo):

```bash
pip install pandas matplotlib seaborn scipy

Execute o script:

python analise_sindrome_gripal.py
