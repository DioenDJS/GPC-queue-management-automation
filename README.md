<h1 align="center">GPC-queue-management-automation</h1>
<!-- <h1 align="center"><img src="" height="60" width="65" alt="" /> NLW 07º HEAT</h1> -->

<p align="center">
    <img src="https://img.shields.io/static/v1?label=DioenD&message=py&color=d2cca1&labelColor=757780" alt="DioenD">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/DioenDJS/GPC-queue-management-automation" >
</p>

## Tecnologias Utilizadas no projeto :construction:

- [Python](https://docs.python.org/3/) <img align="center" alt="img_React" height="40" width="45" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" style="max-width:100%;" />

- [Slack](https://pypi.org/project/slack-sdk/) <img align="center" alt="img_React" height="40" width="45" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/slack/slack-original.svg" style="max-width:100%;" />

- [Cloud Run](https://docs.cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions) <img align="center" alt="img_React" height="40" width="45" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cloudrun/cloudrun-original.svg" style="max-width:100%;" />

- [Langchain](https://docs.langchain.com/oss/python/langchain/quickstart) <img align="center" alt="img_React" height="50" width="55" src="https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/light/langchain-color.png" style="max-width:100%;" />

<img width="1309" height="864" alt="image" src="https://github.com/user-attachments/assets/90445425-b896-404a-8ef4-cf6c0a59bb00" />

## Projeto :computer:
Este projeto implementa uma automação que trata mensagens em filas DLQs (Dead Letter Queues) no Google Cloud.

O fluxo da automação ocorre por meio de um schedule que roda a cada 8 horas, capturando 10 mensagens por requisição. Ele realiza um pull através de um loop em cada subscription existente no projeto; estas mensagens são decodificadas e enviadas para um canal do Slack.

Neste fluxo, existem filas que apresentam erros recorrentes. Elas passam por uma condicional e as que são filtradas acabam sendo enviadas para um Agente de IA. Este agente analisa a fila DLQ de origem para identificar qual subagente é o especialista em analisar e tratar os erros já conhecidos.

Por fim, todas as mensagens são colocadas novamente no tópico de origem através de um endpoint publisher. Logo na sequência, o ackId das mensagens capturadas no início do fluxo é utilizado para deletá-las via rota acknowledge.

### Estrutura do Projeto

```
app/
├── agents/
│   ├── config/
│   │   ├── agent_four.yaml
│   │   ├── agent_one.yaml
│   │   └── system_prompt.yaml
│   ├── skills/
│   │   ├── user_data_processing_skill.py
│   │   └── uuid_approved_processing_skill.py
│   ├── tools/
│   │   ├── mcp_postgres_tool.py
│   │   └── postgres_tool.py
│   └── agent.py
├── common/
│   ├── config/
│   │   └── settings.py
│   ├── utils/
│   │   ├── format_message.py
│   │   └── list_dlqs_and_topic.py
│   └── schemas.py
├── helpers/
│   ├── api_google_cloud.py
│   ├── llms.py
│   └── slack_channel_message.py
├── services/
│   └── process_dlqs.py
└── main.py
```

## CREDENTIALS:
### Export suas credenciais do arquivo json com as permissões do IAM
 * export GOOGLE_APPLICATION_CREDENTIALS="credentials.json"

## Como executar :gear:

> python3 main.py

## Dependências do Projetos :card_index_dividers:

- ### APScheduler 3.11.2
https://pypi.org/project/APScheduler/3.11.2/


## Referencias Documentação:
 ### pull_subscription:
 https://docs.cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/pull?rep_location=global

 ### topic publish
 https://docs.cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/publish?rep_location=global

 ### multi-agent
 https://docs.langchain.com/oss/python/langchain/multi-agent

 ### langchain_ollama
 https://docs.langchain.com/oss/python/integrations/llms/ollama# test_langchain_dlq

 ### langchain_skills
 https://docs.langchain.com/oss/python/langchain/multi-agent/skills

### pg-mcp-server
https://github.com/ericzakariasson/pg-mcp-server
https://github.com/crystaldba/postgres-mcp
