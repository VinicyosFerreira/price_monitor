# Resultado da Task 02 — Dataset fixo de produtos

## Resumo
O projeto foi adaptado para usar um dataset fixo e reproduzível com **500 notebooks**. O Scrapy foi preservado no repositório, mas deixou de ser executado pelo dashboard e pelo job diário.

O novo fluxo é:

```text
fixtures/products.jsonl
        ↓
Transform (Pandas)
        ↓
data/products.csv
        ↓
Dashboard Streamlit
```

A lógica de tratamento da classe `Transform` foi preservada. Apenas o caminho de leitura foi alterado de `data/products.jsonl` para `fixtures/products.jsonl`.

## Pesquisa de mercado utilizada

Os modelos e preços foram inspirados em referências brasileiras reais consultadas em 27/06/2026:

- A Apple apresentou o MacBook Air M4 a partir de R$ 12.999, mostrando que a linha Mac ocupa uma faixa premium: [Apple Brasil](https://www.apple.com/br/newsroom/2025/03/apple-introduces-the-new-macbook-air-with-the-m4-chip-and-a-sky-blue-color/).
- O Dell Inspiron 15 aparecia em configurações entre R$ 3.199 e R$ 4.999: [Dell Brasil](https://www.dell.com/pt-br/shop/notebooks-dell/notebook-inspiron-15/spd/inspiron-15-3530-laptop/brpichbto3530gyrnw6).
- A linha Samsung Galaxy Book apresentava faixa de R$ 3.099 a R$ 16.499: [Samsung Brasil](https://shop.samsung.com/br/informatica/notebooks/galaxy-book).
- A loja HP apresentava desde modelos de entrada próximos de R$ 2.754 até notebooks empresariais e premium acima de R$ 13 mil: [HP Brasil](https://www.hp.com/br-pt/shop/notebook-hp-256-g8-5r5b6la.html).
- A Lenovo posiciona IdeaPad como linha acessível e também oferece famílias gamer: [Lenovo Brasil](https://www.lenovo.com/br/pt/c/laptops/ideapad/).

Essas referências orientaram as diferenças entre notebooks de entrada, intermediários, gamers, empresariais e premium. Os valores da fixture são dados simulados coerentes com o mercado, não ofertas comerciais atuais.

## Arquivo `fixtures/products.jsonl`

O arquivo contém exatamente 500 linhas. Cada linha representa um produto e possui somente os seis campos obrigatórios:

```json
{
  "store": "TechNova Eletrônicos",
  "name": "Notebook Dell Inspiron 15 3530 Core i5 16GB SSD 512GB - Grafite",
  "price": "4.598",
  "currentPrice": "4.598",
  "oldPrice": "4.998",
  "rating": "4.6 (328)"
}
```

## Inconsistências controladas

O dataset possui dados nulos para exercitar as regras existentes do Pandas:

- 22 produtos sem loja (`store: null`);
- 56 produtos sem preço antigo (`oldPrice: null`);
- 46 produtos sem avaliação (`rating: null`).

Durante o ETL, a classe `Transform` aplica suas regras atuais:

- loja nula vira `Loja não informada`;
- avaliação nula vira `Não informado`;
- preço antigo nulo recebe o preço atual.

O campo `currentPrice` nunca é nulo, pois ele é necessário para os cálculos e gráficos do dashboard.

## Formato dos preços
Os preços foram gravados como strings no padrão brasileiro, por exemplo:

```text
"3.199"
"7.499"
"13.999"
```

Essa decisão adapta os dados à implementação existente de `Transform`, que primeiro converte o valor para `float` e depois remove o ponto.

Também foi garantido que nenhum preço termine em zero. Por exemplo, foi usado `"5.149"` em vez de `"5.140"`. Isso é necessário porque o `float` removeria o zero final de `5.140`, e a transformação atual produziria incorretamente `514`. A classe `Transform` permaneceu intocada, conforme exigido.

O campo `price` repete o valor de `currentPrice`. Ele foi mantido porque faz parte obrigatória do novo contrato de dados, embora a transformação atual utilize diretamente `currentPrice` e `oldPrice`.

## Leitura direta do JSONL

O arquivo intermediário `src/fixture_loader.py` foi removido porque deixou de ser necessário.

A classe `Transform` agora lê diretamente:

```text
fixtures/products.jsonl
```

O parâmetro `lines=True` do Pandas continua sendo utilizado, pois cada linha do arquivo contém um objeto JSON independente. Todas as regras de conversão de preços, preenchimento de valores nulos, data e geração do CSV permaneceram iguais.

## Alterações no dashboard

O `app.py` não importa mais `subprocess` nem `sys` e não executa a spider. `Path` é utilizado apenas para verificar se o CSV inicial já existe.

O botão manual de coleta foi removido. Ao iniciar, o aplicativo:

1. verifica se `data/products.csv` já existe;
2. se não existir, executa `Transform` diretamente sobre a fixture JSONL;
3. se já existir, não executa uma nova carga;
4. exibe o dashboard.

Essa verificação evita duplicar 500 registros toda vez que o Streamlit reexecuta a página. As cargas diárias ficam sob responsabilidade exclusiva do scheduler. A lógica repetida de criação da `View` também foi simplificada.

## Alterações no job diário

O arquivo `src/jobs/scheduler.py` não executa mais um subprocesso do Scrapy.

No horário configurado, o job agora:

1. executa a transformação diretamente sobre a fixture JSONL;
2. registra o resultado em log;
3. mantém as duas tentativas adicionais em caso de falha.

O APScheduler, o horário diário, os logs e os retries foram preservados.

## Situação do Scrapy

O Scrapy não foi removido do projeto:

- `Scrapy==2.14.1` continua no `requirements.txt`;
- a pasta `src/collect` continua existente;
- a spider `MercadoLivre` foi preservada.

Ele apenas não participa mais do fluxo principal do `app.py` nem do job diário.

## Validação realizada

Não foram criados testes automatizados ou mocks.

A validação foi feita lendo a fixture JSONL e executando a classe `Transform` real. Resultado:

```text
Produtos na fixture: 500
Lojas informadas diferentes: 25
Campos por produto: 6
Nomes diferentes: 250
Linhas geradas no CSV: 500
Menor preço após o ETL: R$ 2.023
Maior preço após o ETL: R$ 26.999
Preços antigos abaixo do preço atual: 0
Avaliações diferentes após o ETL: 455
Mediana dos produtos Apple: R$ 12.934
Mediana dos demais produtos: R$ 5.246
Maior quantidade em uma loja: 38
Menor quantidade em uma loja: 2
Campos diferentes de store alterados na conversão: 0
```

Também foi executada a compilação de sintaxe de `app.py`, `src/transform/main.py` e `src/jobs/scheduler.py`, sem erros.

O carregamento automático do aplicativo também foi executado duas vezes sobre um CSV existente: a quantidade permaneceu em 500 linhas, confirmando que o rerun do Streamlit não dispara uma nova carga nem duplica os registros.

## Como executar

Na raiz do projeto, ative o ambiente virtual e instale as dependências:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Inicie o dashboard:

```powershell
streamlit run app.py
```

Na primeira abertura, os dados são preparados automaticamente. Não existe botão de coleta ou processamento.

Para iniciar o job diário em outro terminal:

```powershell
python -m src.jobs.scheduler
```

O job permanece em execução e processa os dados diariamente no horário configurado.

## Arquivos criados

- `fixtures/products.jsonl`: dataset fixo com 500 produtos, um por linha;
- `tasks/result_02.md`: documentação desta implementação.

## Arquivos modificados

- `app.py`: remove o consumo do Scrapy e usa a fixture;
- `src/transform/main.py`: passa a ler diretamente `fixtures/products.jsonl`;
- `src/jobs/scheduler.py`: processa a fixture no job diário;
- `README.md`: atualiza arquitetura e instruções de execução.

## Critérios de aceite

- 500 produtos exatos: **atendido**.
- Campos `store`, `name`, `price`, `currentPrice`, `oldPrice` e `rating`: **atendido**.
- Entre 20 e 30 lojas: **atendido com 25 lojas informadas**.
- Dados nulos para tratamento: **atendido**.
- Diversidade de marcas, preços e avaliações: **atendido**.
- Coerência com o mercado brasileiro: **atendido com pesquisa de referência**.
- Regras de transformação preservadas: **atendido; somente o caminho da fonte passou a apontar para a fixture JSONL**.
- Sem testes automatizados: **atendido**.
- Scrapy preservado, mas fora do consumo principal: **atendido**.
- Arquitetura atual preservada: **atendido**.
