# Resultado da Task 01 — Job diário de coleta

## O que foi criado

Foi criado um job com **APScheduler** para executar automaticamente a coleta e a transformação dos preços uma vez por dia.

O arquivo responsável pelo job é:

```text
src/jobs/scheduler.py
```

O `app.py` não foi alterado. Ele continua responsável pelo dashboard Streamlit e pela coleta manual através do botão.

## Como o job funciona

O fluxo automático segue esta ordem:

1. O `scheduler.py` fica aguardando o horário programado.
2. Às 08:00, ele inicia a spider `MercadoLivre` do Scrapy.
3. A spider grava os dados coletados em `data/products.jsonl`.
4. A classe `Transform` trata os dados.
5. O resultado tratado é salvo em `data/products.csv`.
6. O andamento é registrado em `logs/scheduler.log`.

Se alguma etapa falhar, o sistema espera cinco minutos e tenta novamente. Ele faz uma execução inicial e, se necessário, mais duas tentativas.

```text
Execução inicial
    └── falhou → tentativa 2
                      └── falhou → tentativa 3
                                        └── falhou → encerra e registra o erro
```

## Primeira execução

Abra o PowerShell na pasta do projeto e ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Inicie o job:

```powershell
python -m src.jobs.scheduler
```

O terminal deve mostrar uma mensagem informando que o agendador foi iniciado e que a execução diária está programada para 08:00.

O terminal precisa permanecer aberto. Para encerrar o job, pressione `Ctrl+C`.

## Como abrir o dashboard

O job e o dashboard são processos separados. Abra outro terminal, ative o mesmo ambiente virtual e execute:

```powershell
streamlit run app.py
```

Assim, cada arquivo tem uma responsabilidade simples:

- `src/jobs/scheduler.py`: realiza a coleta automática diária;
- `app.py`: abre o dashboard e mantém o botão de coleta manual.

Não é recomendado iniciar o APScheduler dentro do `app.py`, porque o Streamlit executa novamente o arquivo sempre que a tela muda. Isso poderia criar mais de um agendamento por engano.

## Horário de execução

O horário padrão é 08:00, usando o fuso horário `America/Sao_Paulo`.

Para mudar temporariamente o horário, defina as variáveis antes de iniciar o job. Exemplo para 14:30:

```powershell
$env:SCHEDULE_HOUR = "14"
$env:SCHEDULE_MINUTE = "30"
python -m src.jobs.scheduler
```

Se essas variáveis não forem definidas, o horário continuará sendo 08:00.

## Logs

Os registros são gravados em:

```text
logs/scheduler.log
```

Cada registro contém:

- data e hora;
- nível do registro, como `INFO` ou `ERROR`;
- mensagem explicando o que aconteceu;
- detalhes técnicos da exceção quando houver falha.

A pasta `logs/` foi adicionada ao `.gitignore`. Portanto, os logs permanecem apenas no computador e não são enviados ao GitHub.

## Tentativas após uma falha

O intervalo padrão entre as tentativas é de 300 segundos, ou cinco minutos.

Para alterar temporariamente esse intervalo, use:

```powershell
$env:RETRY_DELAY_SECONDS = "60"
python -m src.jobs.scheduler
```

Nesse exemplo, o sistema esperará 60 segundos entre as tentativas.

## Imports do APScheduler

Os imports utilizados são:

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
```

Eles estão corretos para o APScheduler 3.11.2. O erro encontrado acontecia porque a biblioteca ainda não estava instalada no ambiente virtual `.venv` do projeto.

O pacote foi adicionado ao `requirements.txt` e instalado na `.venv`. Os dois imports e a criação do job foram validados com sucesso.

Se o editor ainda mostrar uma linha vermelha, confirme se ele está usando este interpretador Python:

```text
.venv/Scripts/python.exe
```

Depois, reinicie o editor ou recarregue a janela para que ele reconheça a biblioteca instalada.

## Validação executada e resultado real

Não foi criada uma suíte de testes automatizados e não foram utilizados mocks, conforme solicitado.

A validação foi feita manualmente em 27/06/2026, usando o ambiente virtual real do projeto.

### 1. Imports e criação do agendamento

Foram importadas as classes `BlockingScheduler` e `CronTrigger` e o job foi criado diretamente com o Python da `.venv`.

Resultado:

```text
Imports funcionando
daily_price_monitoring
cron[hour='8', minute='0']
```

Essa etapa foi concluída com sucesso. Ela confirma que o APScheduler está instalado e que existe um job diário configurado para 08:00.

### 2. Execução real da coleta e transformação

A pipeline foi executada de verdade, sem mock. O Scrapy iniciou normalmente, mas a spider atual não encontrou produtos. O arquivo `data/products.jsonl` foi criado vazio, com zero bytes.

Também foi executado exatamente o comando que já existia no botão do `app.py`:

```powershell
python -m scrapy crawl MercadoLivre -o ../../data/products.jsonl
```

Ele foi executado a partir da pasta `src/collect`, usando o mesmo Python da `.venv`. O resultado também foi zero produtos. As estatísticas do Scrapy mostraram:

```text
Redirecting (302) to /gz/account-verification
Stored jsonl feed (0 items)
items_per_minute: 0.0
```

Isso confirma que o problema não está no `sys.executable`, no diretório de execução nem na chamada criada no scheduler. Na validação atual, o Mercado Livre redirecionou a requisição para uma página de verificação de conta. Essa página não contém os cards de produtos esperados pela spider.

Resultado:

```text
RuntimeError: A coleta terminou, mas não retornou nenhum produto.
```

Foi adicionada uma validação no job para detectar esse caso antes de chamar a classe `Transform`. Isso evita o erro menos claro `KeyError: 'currentPrice'` que ocorria quando o Pandas tentava ler uma coleta vazia.

### 3. Tentativas após a falha

O job foi executado com intervalo temporário de zero segundos apenas para validar as tentativas sem esperar dez minutos. A execução real apresentou esta sequência:

```text
Execução 1 de 3 → falhou
Execução 2 de 3 → falhou
Execução 3 de 3 → falhou
Pipeline encerrada após 3 falhas
```

Essa etapa confirmou que o job faz exatamente duas tentativas adicionais e registra todas as falhas em `logs/scheduler.log`.

### Situação final da validação

- Imports do APScheduler: **funcionando**.
- Criação do job diário: **funcionando**.
- Horário diário às 08:00: **configurado corretamente**.
- Logs: **funcionando**.
- Duas tentativas adicionais: **funcionando**.
- Coleta completa até a transformação: **não concluída**, porque a spider existente retornou zero produtos.

O agendador está funcionando e tratou corretamente a falha. Porém, não é correto afirmar que a pipeline completa terminou com sucesso enquanto a spider não retornar produtos. A causa confirmada nesta execução foi o redirecionamento do Mercado Livre para a página `/gz/account-verification`. Esse comportamento deverá ser analisado na camada `src/collect`.

## Diferença entre `-o` e `-O`

O botão do `app.py` utiliza `-o` minúsculo. Esse parâmetro adiciona os novos itens ao arquivo que já existe. Caso a coleta retorne zero itens, os produtos antigos continuam no JSON e ainda podem ser transformados e exibidos. Isso pode dar a impressão de que uma nova coleta funcionou.

O job utiliza `-O` maiúsculo. Esse parâmetro substitui o JSON a cada coleta. Assim, o job não reaproveita silenciosamente produtos antigos quando a coleta atual falha e não duplica todo o conteúdo bruto no processamento diário.

## Computador desligado

O APScheduler funciona enquanto o computador estiver ligado e o comando abaixo estiver executando:

```powershell
python -m src.jobs.scheduler
```

Se o computador estiver desligado às 08:00, a coleta não acontecerá naquele horário. Para uma execução contínua, o projeto deverá ficar em uma máquina ou servidor que permaneça ligado.

## Arquivos alterados

- `src/jobs/scheduler.py`: implementação do job diário;
- `src/jobs/__init__.py`: identifica `jobs` como pacote Python;
- `requirements.txt`: adiciona `APScheduler==3.11.2`;
- `.gitignore`: ignora a pasta `logs/`;
- `tasks/result_01.md`: documentação da implementação.
