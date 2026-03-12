# 📈 Monitoramento de Preços RPA & Analytics

Este projeto é uma solução robusta de RPA (Robotic Process Automation) para monitoramento e análise de preços, automatizando em 100% o processo manual. Através de uma pipeline ETL (Extract, Transform, Load), a ferramenta viabiliza inteligência de mercado em tempo real com uma interface visual intuitiva.

## 🚀 Tecnologias
**Python**: Linguagem core para execução da lógica e automação.

**Scrapy**: Framework de alto desempenho para extração de dados via Web Scraping.

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
data/             # Arquivos JSONL e CSV (Persistência local)
src/
├── collect/      # Spiders do Scrapy para extração de dados
├── transform/    # Lógica de ETL e limpeza com Pandas
├── view/         # Interface e Dashboard com Streamlit
└── static/       # Ativos estáticos
```

## 🗺️ Fluxo de Valor (ETL)

🤖 **Coleta de Dados**: Implementação de spiders otimizadas com Scrapy que colaboram para uma extração de alto volume via requisições assíncronas, capturando milhares de registros em cerca de 15 segundos.

🧹 **Transformação de Dados**: Camada responsável por redesenhar os dados brutos. Utiliza DataFrames para limpeza de valores nulos, tratamento de duplicatas e formatação monetária.

📊 **Visualização Analytics**: Dashboard interativo que transforma dados em decisão. Utiliza Streamlit para exibir métricas de KPI, tabelas filtráveis e gráficos de dispersão que mostram a realidade do mercado.

## 📦Rodar o projeto
Para executar o projeto, siga os seguintes passos:

Certifique-se de ter o Python instalado em sua máquina

`https://www.python.org/downloads/`

Clone este repositório para o seu computador.

`git clone https://github.com/VinicyosFerreira/price_monitor`

Instale as dependências do projeto.

`pip install -r requirements.txt`

Coleta de dados via scrapy na pasta (src/collect).Será gerado a pasta data com arquivo JSON.

`scrapy crawl MercadoLivre -o ../../data/products.jsonl`

Limpeza e transformação de dados na pasta(src/transform).Será gerado na pasta data um csv com dados.

`python main.py`

Execução do dashboard na pasta (src/view)

`streamlit run main.py`

## 🔗 Links 
**Código Fonte**

https://github.com/VinicyosFerreira/price_monitor
