# 📈 Monitoramento de Preços RPA & Analytics

Este projeto é uma solução de RPA (Robotic Process Automation) para processamento e análise de preços. Através de uma pipeline ETL (Extract, Transform, Load).

## 🚀 Tecnologias
**Python**: Linguagem core para execução da lógica e automação.

**Scrapy**: Framework preservado como integração experimental de Web Scraping.

**Pandas**: Biblioteca poderosa para limpeza, manipulação e estruturação de dados.

**Streamlit**: Framework para criação de dashboards interativos e interfaces web.

**Plotly**: Geração de gráficos dinâmicos para análise de dispersão de preços.

## 📈 Métricas e Resultados
- ### Automatização de 100% de processos manuais;
- ### Milhares de dados processados em segundos;
- ### Customizável para diferentes modelos de negócios.


## 📊 Gif da Dashboard
<div class="text-center">
  <img src="./src/static/ui.gif" alt="Demonstração do Dashboard" width="100%">
</div>


## 📁 Estrutura do Projeto
```
fixtures/         # Dataset
data/             # CSV processado e gerado localmente
src/
├── collect/      # Spider preservada como integração experimental
├── jobs/         # Agendamento diário, logs e retries
├── transform/    # Lógica de ETL e limpeza com Pandas
├── view/         # Interface e Dashboard com Streamlit
└── static/       # Ativos estáticos
```

## 🗺️ Fluxo de Valor (ETL)

🤖 **Extração de Dados**: Leitura de 500 produtos diretamente de `fixtures/products.jsonl`. O dataset contém preços, lojas, avaliações e inconsistências controladas para exercitar o tratamento de dados.

🧹 **Transformação de Dados**: Camada responsável por redesenhar os dados brutos. Utiliza DataFrames para limpeza de valores nulos, tratamento de duplicatas e formatação monetária.

📊 **Visualização Analytics**: Dashboard interativo que transforma dados em decisão. Utiliza Streamlit para exibir métricas de KPI, tabelas filtráveis e gráficos de dispersão que mostram a realidade do mercado.

## 📦Rodar o projeto
Para executar o projeto, siga os seguintes passos:

Certifique-se de ter o Python instalado em sua máquina

`https://www.python.org/downloads/`

Clone este repositório para o seu computador.

`git clone https://github.com/VinicyosFerreira/price_monitor`

Instale as dependências do projeto.

`python -m pip install -r requirements.txt`

Execute o dashboard na raiz do projeto:

`streamlit run app.py`

Na primeira execução, o aplicativo executa o ETL diretamente sobre a fixture JSONL. Nas execuções seguintes, ele apenas carrega o CSV já processado.

Para manter a carga diária agendada às 08:00, execute em outro terminal:
`python -m src.jobs.scheduler`

## 🔗 Links 
**Código Fonte**
https://github.com/VinicyosFerreira/price_monitor
