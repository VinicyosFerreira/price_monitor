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
- Criar um JSON fixo para listagem de produtos em fixtures/products.json, ele deve conter exatamente o mesmo esqueleto antigo, com os campos `store, name, price, currentPrice, oldPrice, rating` **OBRIGATORIAMENTE**
- Deve conter alguns campos null/none para permitir tratamento de dados e simulação de dados incosistentes para tratamento de acordo com transform do Pandas
- **EXEMPLOS**: loja não informada e preços antigos não informados

## Regras
- Deve conter 500 produtos exatamente com descritos acima
- Deve conter 20 a 30 lojas, **NÃO PODENDO SER MENOS OU MAIS**, use nomes diversificados e marcas reais como Samsung, LG, MAC para nome de produtos e lojas pode usar nomes ficticios porém **SEM** nomes incoerente com lojas de eletrônicos
- Faça pesquisa na **internet** para consultar preços de notebooks reais na web/nome de lojas para inspiração para considerar um em cenário real(Tipo Mac é mais caro que Windows e seja coerente com **REGRA DO MERCADO BRASILEIRO**)
- Utilize diversificação em avaliações no campo rating e preços para evitar resultados fracos para ETL
- **NUNCA** mude o código na class Transform do Pandas, faça os dados do JSON se adaptarem a lógica já existente

## Critérios de aceite
- Os dados devem ser estritamente coerente com a regra do mercado(marcas consolidadas, nome de loja aderentes e
preços ideais seguindo uma regra de marketplace)
- **NÃO IMPLEMENTE** TESTES AUTOMATIZADOS
- Adapte sem mexer em regras arquiteturais de forma brusca, **APENAS** no necessário
- Remoção de trechos de códigos que não será utilizados conforme adaptação 
- Mantenha o scrapy apenas remova dos arquivos importados e lógica de consumo

## Consequências
- O código deve estar 100% adequados com as regras/descrições acima

## Output
- Escreva a implementação detalhada e clara como **SE** estivesse explicando para um desenvolvedor júnior no arquivo `result_02.md`## Critérios de aceite
- A implementação deve preservar a arquitetura atual do projeto.

