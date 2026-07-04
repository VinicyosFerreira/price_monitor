## Role

Você é um desenvolvedor sênior em automação(RPA) e especializado em análise e engenharia de dados.

## Contexto

O projeto é uma RPA (Robotic Process Automation) para monitoramento e análise de preços, automatizando em 100% o processo manual. Através de uma pipeline ETL (Extract, Transform, Load), a ferramenta viabiliza inteligência de mercado em tempo real com uma interface visual intuitiva.

## Tecnologias Utilizadas

- Python
- Scrapy
- Pandas
- Streamlit
- Plotly

## Tarefa
Implementar uma lógica para geração dinâmica do arquivo `src/data/products.jsonl` utilizando como base uma fixture fixa.

A implementação deve:
- Ler a fixture contendo exatamente 500 produtos.
- Gerar uma nova versão do arquivo a cada execução do job agendado.
- Aplicar variações inteligentes em `currentPrice` e `oldPrice`, simulando oscilações naturais de mercado.
- Simular diferentes cenários, como estabilidade de preço, pequenas altas, pequenas quedas e promoções ocasionais. **UTILIZE** métodos claros para realizar a implementação.
- Inserir alguns valores `null` em campos `currentPrice` para permitir a validação do tratamento realizado pela classe `Transform`.
- Garantir o fluxo completo end to end funcional, integrando com Transform(Pandas) e Jobs(ApScheduler)
- Preservar o schema atual esperado pelo pipeline ETL.
- Salvar o resultado em `src/data/products.jsonl`.

## Regras
- Gerar exatamente 500 produtos.
- Utilizar sempre a fixture como fonte de dados.
- Não alterar nome, categoria, identificadores ou demais informações estáticas dos produtos.
- Alterar apenas campos relacionados à dinâmica de mercado, como `currentPrice` e `oldPrice`.
- Manter coerência de mercado em todas as execuções.
- Evitar oscilações bruscas e preços incompatíveis com o tipo do produto por exemplo notebooks custando extremos para baixo R$100 ou máximo extremo R$100.000, por exemplo
- Permitir promoções e reajustes ocasionais, porém controlados.
- A implementação **DEVE SER** na classe `Extractor` no arquivo `main.py` na pasta `extract` que comecei a esboçar, sendo responsável apenas pela geração do arquivo dinâmico com lógica para mudanças nos preços.

## Critério de aceite
[ ] - **NÃO IMPLEMENTE** TESTES AUTOMATIZADOS.
[ ] - Adapte sem mexer em regras arquiteturais de forma brusca, **APENAS** no necessário.
[ ] - Lógica aderente a tarefa solicitada e foco em código limpo e escalável.

## Output
- Escreva a implementação direta e clara como **SE** estivesse explicando para um desenvolvedor júnior no arquivo `result_03.md` na pasta `src/tasks`


