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
Criar um job/scheduled automatizado para gatilho inicial da automação, a idéia é que tarefa seja executado uma única vez por dia de forma automatizada a fim da coleta ser totalmente gerenciável. Onde possa haver registro de logs a fim de validação se foi executado com sucesso ou houve falha da tarefa. Em caso de falha deve ser usado retry novamente 2x após para averiguar se foi falha temporária ou incidente maior registrado.

## Regras
- Utilize **APENAS** o APScheduler para a tarefa, **NÃO** outra ferramenta como Celery,Cron,Task Scheduler do Windows ou outra ferramenta de agendamento.
- Utilize a lib **logging** nativa do Python inicialmente para registrar na pasta `/logs` como hora, nível e mensagem de erros das execuções. COLOCAR OBRIGATORIAMENTE no .gitignore a pasta, **NÃO** deve subir para o Github. 
- Crie uma pasta `/logs`, evite mexer na arquitetura atual, integre **APENAS** o necessário sem mudanças bruscas que possam afetar o entendimento técnico futuro.
- Utilize código simples de entender, **EVITE** lógicas complexas e repetição de código, priorize clareza e código limpo seguindo princípios de programação como Clean Code.


## Consequências
- O código deve estar 100% funcional e testado e com instruções de execução.

## Output
- Escreva a implementação detalhada e clara como **SE** estivesse explicando para um desenvolvedor júnior no arquivo `result_01.md`## Critérios de aceite
- O job deve executar automaticamente uma vez por dia.
- Deve utilizar exclusivamente APScheduler.
- Deve registrar logs em `/logs`.
- A pasta `/logs` deve estar no `.gitignore`.
- Em caso de falha, deve realizar até 2 tentativas adicionais.
- A implementação deve preservar a arquitetura atual do projeto.