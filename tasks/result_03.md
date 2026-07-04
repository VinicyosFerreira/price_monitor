# Resultado da tarefa 03 — geração dinâmica de preços

## 1. Objetivo da implementação

Esta tarefa adiciona uma etapa de extração dinâmica ao pipeline ETL. Antes, o `Transform` lia diretamente a fixture fixa. Agora, a fixture continua sendo a fonte oficial dos 500 produtos, mas o `Extractor` cria uma nova fotografia de mercado antes de cada processamento agendado.

Essa fotografia é salva em `data/products.jsonl`. Ela mantém os dados fixos dos produtos e altera somente `currentPrice` e `oldPrice`, simulando estabilidade, reajustes, quedas e promoções.

É importante diferenciar os dois arquivos:

- `fixtures/products.jsonl`: base fixa e imutável, usada como referência em todas as execuções;
- `data/products.jsonl`: resultado dinâmico, recriado pelo `Extractor` a cada execução.

Usar sempre a fixture como ponto de partida impede o efeito de preço acumulado. Por exemplo, se uma alta de 5% fosse aplicada diariamente sobre o arquivo do dia anterior, o preço poderia crescer de forma artificial. Na solução implementada, cada execução recomeça do preço original do produto.

## 2. Arquivos alterados

### `src/extract/main.py`

Contém toda a responsabilidade de gerar o JSONL dinâmico. A classe `Extractor` lê a fixture, valida os dados, calcula os novos preços e salva o resultado.

### `src/transform/main.py`

O construtor de `Transform` passou a aceitar o argumento opcional `source_path`. Dessa forma, o transformador pode receber explicitamente o arquivo criado pelo `Extractor`:

```python
Transform(source_path=products_path).execute()
```

Quando nenhum caminho é informado, o valor padrão é `data/products.jsonl`, na pasta `data` da raiz do projeto. Também foi adicionada a criação da pasta de destino antes de salvar o CSV.

### `src/jobs/scheduler.py`

O job diário agora executa a extração antes da transformação. A ordem passou a ser:

```python
products_path = Extractor().execute()
Transform(source_path=products_path).execute()
```

Isso garante que toda execução do APScheduler produza uma nova fotografia de preços. Se alguma etapa lançar uma exceção, o mecanismo de tentativas que já existia no scheduler repete o pipeline completo, respeitando o limite e o intervalo configurados.

### `app.py`

A preparação inicial do Streamlit também foi integrada ao novo fluxo. Quando `data/products.csv` ainda não existe, a aplicação gera primeiro o JSONL dinâmico e somente depois executa o `Transform`.

## 3. Estrutura da classe `Extractor`

### Constantes de caminhos e quantidade

O arquivo define três constantes principais:

```python
FIXTURE_PATH = ROOT_PATH / "fixtures" / "products.jsonl"
OUTPUT_PATH = ROOT_PATH / "data" / "products.jsonl"
EXPECTED_PRODUCT_COUNT = 500
```

Centralizar esses valores evita espalhar caminhos e números fixos pelo código. Se o local do arquivo mudar no futuro, existe apenas um ponto principal para ajustar.

### Método `__init__`

O construtor recebe três dependências opcionais:

- `fixture_path`: caminho da fixture de entrada;
- `output_path`: caminho do JSONL que será gerado;
- `random_generator`: gerador responsável pelos sorteios.

Na execução normal, não é necessário informar nenhum deles:

```python
extractor = Extractor()
```

O `random_generator` opcional deixa a classe mais flexível, pois permite fornecer um `random.Random` configurado quando for necessário reproduzir uma sequência conhecida durante uma análise manual.

### Método `extract`

Esse método abre a fixture com codificação UTF-8 e lê cada linha separadamente. Como o formato é JSONL, cada linha representa um objeto JSON completo:

```python
products = [json.loads(line) for line in file if line.strip()]
```

Linhas vazias são ignoradas. Depois da leitura, a quantidade é validada. Se forem encontrados mais ou menos de 500 produtos, o método interrompe o fluxo com `ValueError`.

Essa validação é importante porque o restante do pipeline depende da regra de gerar exatamente 500 registros. Continuar silenciosamente com uma fixture incompleta poderia produzir indicadores incorretos no dashboard.

### Método `_parse_price`

Os preços da fixture são textos no padrão brasileiro, como `"6.439"`. Para realizar cálculos, esse valor precisa virar um número. O método remove o separador de milhar e converte o resultado para `float`:

```text
"6.439" → "6439" → 6439.0
```

Ele também aceita valores que já sejam `int` ou `float`. Um preço ausente ou menor ou igual a zero gera uma exceção, porque não seria uma base válida para calcular oscilações.

### Método `_format_price`

Depois dos cálculos, o preço precisa voltar ao formato esperado pelo pipeline:

```text
6439.0 → "6.439"
```

O método arredonda o valor para uma unidade inteira, garante um mínimo de 1 e aplica o ponto como separador de milhar. Assim, o schema e o padrão monetário permanecem compatíveis com o `Transform` existente.

## 4. Cenários de mercado implementados

Cada cenário fica em um método próprio. Essa separação torna o código mais fácil de ler, manter e ampliar. Todos recebem o preço base e retornam uma tupla na ordem:

```python
(currentPrice, oldPrice)
```

### `_stable_price`

Representa um produto praticamente estável. A variação sorteada fica entre -0,5% e +0,5%.

```text
preço atual = preço base × (1 + variação entre -0,005 e 0,005)
```

Nesse cenário, `currentPrice` e `oldPrice` recebem o mesmo resultado, indicando que não existe uma diferença comercial relevante entre os dois valores.

Exemplo aproximado: um item de R$ 6.000 pode ficar entre R$ 5.970 e R$ 6.030.

### `_small_increase`

Simula um reajuste leve entre 1% e 5%.

```text
currentPrice = preço base × (1 + percentual entre 0,01 e 0,05)
oldPrice = preço base
```

Exemplo: um item de R$ 6.000 pode passar para um valor entre R$ 6.060 e R$ 6.300.

### `_small_drop`

Simula uma queda normal de mercado entre 1% e 6%.

```text
currentPrice = preço base × (1 - percentual entre 0,01 e 0,06)
oldPrice = preço base
```

Exemplo: um item de R$ 6.000 pode passar para um valor entre R$ 5.640 e R$ 5.940.

### `_promotion`

Representa uma promoção ocasional. Primeiro é calculado um preço anterior entre 2% e 8% acima da base. Em seguida, um desconto entre 10% e 20% é aplicado sobre esse preço anterior:

```text
oldPrice = preço base × (1 + percentual entre 0,02 e 0,08)
currentPrice = oldPrice × (1 - desconto entre 0,10 e 0,20)
```

Com isso, `oldPrice` fica maior que `currentPrice`, comportamento esperado para exibir uma oferta.

## 5. Como um cenário é escolhido

O método `generate_price` percorre os 500 produtos e utiliza `random.choices` para selecionar um cenário. Os pesos configurados são:

| Cenário | Peso | Tendência esperada |
|---|---:|---:|
| Estabilidade | 55 | aproximadamente 55% |
| Pequena alta | 15 | aproximadamente 15% |
| Pequena queda | 22 | aproximadamente 22% |
| Promoção | 8 | aproximadamente 8% |

Esses valores são probabilidades, não quantidades fixas. Em uma execução podem existir, por exemplo, 39 promoções e, em outra, 43. Essa variação faz parte da simulação natural do mercado.

A estabilidade possui o maior peso porque, em um cenário real, a maioria dos produtos não sofre uma mudança relevante todos os dias. Promoções são menos frequentes para não transformar todo o catálogo em oferta.

## 6. Preservação dos dados estáticos

Dentro do laço, cada produto é copiado antes da alteração:

```python
product = original.copy()
```

Depois disso, somente estes campos recebem novos valores:

```python
product["currentPrice"] = ...
product["oldPrice"] = ...
```

Campos como `store`, `name`, `price` e `rating` não são modificados. A cópia também evita alterar em memória o dicionário que representa a linha original da fixture.

O preço usado como referência é `currentPrice`. Caso ele esteja vazio na fixture, o código usa `price` como alternativa:

```python
base = self._parse_price(product.get("currentPrice") or product.get("price"))
```

## 7. Inserção controlada de valores nulos

Depois que todos os preços são gerados, o método calcula 2% da quantidade de produtos:

```text
500 × 2% = 10 produtos
```

Dez índices diferentes são escolhidos com `random.sample`, e somente o `currentPrice` desses produtos passa a ser `None`. Ao salvar como JSON, `None` é convertido corretamente para `null`.

O uso de `random.sample` é importante porque ele não repete índices. Portanto, sempre existem exatamente 10 produtos distintos com `currentPrice` nulo na saída de 500 registros.

Esses valores não representam uma falha do gerador. Eles foram inseridos de propósito para exercitar o tratamento de dados ausentes do `Transform`. Durante a conversão com Pandas, esses valores tornam-se ausentes e seguem o tratamento numérico já existente no pipeline.

## 8. Salvamento seguro com `save`

Antes de escrever o resultado, o método valida novamente se a lista contém exatamente 500 produtos. Essa segunda verificação protege a saída caso `save` seja chamado diretamente com uma lista incorreta.

A pasta `data` da raiz do projeto é criada automaticamente se ainda não existir:

```python
self.output_path.parent.mkdir(parents=True, exist_ok=True)
```

O conteúdo é escrito primeiro em `products.jsonl.tmp`. Somente depois de todas as 500 linhas serem gravadas, o arquivo temporário substitui `products.jsonl`:

```text
products.jsonl.tmp → products.jsonl
```

Essa estratégia reduz o risco de o `Transform` encontrar um arquivo incompleto se ocorrer uma falha durante a escrita. Cada produto é serializado com `ensure_ascii=False`, preservando corretamente caracteres como acentos nos nomes e lojas.

No final, `save` retorna um objeto `Path` com o caminho do arquivo gerado. Esse retorno é usado pelo scheduler e pelo aplicativo para indicar ao `Transform` exatamente qual arquivo deve ser lido.

## 9. Método principal `execute`

O método `execute` funciona como a porta de entrada da classe e encadeia as três responsabilidades na ordem correta:

```python
return self.save(self.generate_price(self.extract()))
```

Para um iniciante, a leitura dessa linha ocorre de dentro para fora:

1. `extract()` lê e valida a fixture;
2. `generate_price(...)` cria os novos preços e os valores nulos;
3. `save(...)` grava o resultado em `data/products.jsonl`;
4. o caminho do arquivo é devolvido para quem chamou `execute()`.

Também é possível executar somente a extração pelo terminal:

```bash
python -m src.extract.main
```

Nesse caso, o arquivo é gerado e seu caminho é exibido no terminal.

## 10. Fluxo end to end completo

O fluxo diário ficou assim:

```text
APScheduler
    ↓
run_with_retry()
    ↓
run_pipeline()
    ↓
Extractor.execute()
    ├── lê fixtures/products.jsonl
    ├── valida 500 produtos
    ├── gera cenários de preço
    ├── insere 10 currentPrice nulos
    └── salva data/products.jsonl
    ↓
Transform(source_path=products_path).execute()
    ├── lê o JSONL dinâmico com Pandas
    ├── aplica limpeza e conversões
    ├── adiciona a data da análise
    └── grava ou acrescenta dados em data/products.csv
    ↓
Streamlit utiliza o CSV processado no dashboard
```

Se o `Extractor` falhar, o `Transform` não é executado com dados incompletos. A exceção volta para `run_with_retry`, que registra o erro e realiza uma nova tentativa conforme a configuração do scheduler.

## 11. Garantias atendidas

- A fixture continua sendo a única fonte dos produtos.
- Exatamente 500 registros são exigidos na entrada e na saída.
- O arquivo dinâmico é recriado em cada execução do job.
- Somente `currentPrice` e `oldPrice` são alterados.
- Os demais campos e o schema original são preservados.
- As variações usam percentuais pequenos sobre o preço de cada produto.
- Os preços não acumulam oscilações de execuções anteriores.
- Promoções são ocasionais e possuem desconto controlado.
- Exatamente 10 produtos recebem `currentPrice: null` em cada geração.
- O salvamento temporário reduz o risco de arquivos parciais.
- O `Extractor`, o `Transform`, o APScheduler e a carga inicial do Streamlit estão integrados.
- Nenhum teste automatizado foi criado, conforme solicitado na tarefa.

## 12. Validação manual realizada

Após a implementação, o fluxo foi executado manualmente. A verificação confirmou:

- geração de 500 linhas em `data/products.jsonl`;
- presença de 10 valores nulos em `currentPrice`;
- manutenção do mesmo conjunto de campos da fixture;
- execução bem-sucedida do `Transform` sobre o arquivo dinâmico.
