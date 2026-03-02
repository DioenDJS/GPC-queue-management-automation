<h1 align="center">GPC-queue-management-automation</h1>
<!-- <h1 align="center"><img src="" height="60" width="65" alt="" /> NLW 07º HEAT</h1> -->

<p align="center">
    <img src="https://img.shields.io/static/v1?label=DioenD&message=py&color=d2cca1&labelColor=757780" alt="DioenD">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/DioenDJS/GPC-queue-management-automation" >
</p>

## Tecnologias Utilizadas no projeto :construction:

- [Python](https://docs.python.org/3/) <img align="center" alt="img_React" height="40" width="45" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" style="max-width:100%;" />


## Projeto :computer:
Este projeto implementa uma automação que trata mensagens em filas DLQs (Dead Letter Queues) no Google Cloud.

O fluxo da automação ocorre por meio de um schedule que roda a cada 8 horas, capturando 10 mensagens por requisição. Ele realiza um pull através de um loop em cada subscription existente no projeto; estas mensagens são decodificadas e enviadas para um canal do Slack.

Neste fluxo, existem filas que apresentam erros recorrentes. Elas passam por uma condicional e as que são filtradas acabam sendo enviadas para um Agente de IA. Este agente analisa a fila DLQ de origem para identificar qual subagente é o especialista em analisar e tratar os erros já conhecidos.

Por fim, todas as mensagens são colocadas novamente no tópico de origem através de um endpoint publisher. Logo na sequência, o ackId das mensagens capturadas no início do fluxo é utilizado para deletá-las via rota acknowledge.

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
