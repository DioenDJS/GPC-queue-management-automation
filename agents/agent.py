import json
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool

from agents.skills.user_data_processing_skill import user_data_processing_skill
from agents.skills.uuid_approved_procesing_skill import uuid_approved_processing_skill
from agents.tools.mcp_postgres_tool import get_mcp_postgres_tool
from agents.tools.postgres_tool import get_postgres_tool
from helpers.llms import LLMProvider, Llms
from helpers.slack_channel_message import SlackChannelMessage

base_dir = Path(__file__).resolve().parent

slack_api = SlackChannelMessage()

agent_queue_one = create_agent(
    model=Llms(provider=LLMProvider.OLLAMA_GLM_5_CLOUD).get_llm(),
    name="agent_queue_one",
    system_prompt=(base_dir / "config" / "agent_one.yaml").read_text(),
    tools=[get_mcp_postgres_tool, user_data_processing_skill],
)

agent_queue_four = create_agent(
    model=Llms(provider=LLMProvider.OLLAMA_GLM_5_CLOUD).get_llm(),
    name="agent_fila_quatro",
    system_prompt=(base_dir / "config" / "agent_four.yaml").read_text(),
    tools=[get_postgres_tool, uuid_approved_processing_skill],
)


@tool(
    "analysis_queue_one",
    description="Subagente especializado em analisar mensagens de erro da "
    "fila um (subscription-fila-um-dlq). Use para erros relacionados à fila um.",
)
def call_analysis_queue_one_subagent_one(query: str):
    result = agent_queue_one.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool(
    "analysis_queue_four",
    description="Subagente especializado em analisar mensagens de erro da "
    "fila quatro (subscription-fila-quatro-dlq). Use para erros relacionados à fila quatro.",
)
def call_analysis_queue_one_subagent_four(query: str):
    result = agent_queue_four.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


def call_agent(query: str):
    query_dict = json.loads(query)
    main_agent = create_agent(
        model=Llms(provider=LLMProvider.OLLAMA_GLM_5_CLOUD).get_llm(),
        tools=[
            call_analysis_queue_one_subagent_one,
            call_analysis_queue_one_subagent_four,
        ],
        system_prompt=(base_dir / "config" / "system_prompt.yaml").read_text(),
    )
    result = main_agent.invoke({"messages": [{"role": "user", "content": query}]})

    msg = {
        "content": result["messages"][-1].content,
        "dlq": query_dict.get("dlq", ""),
    }
    slack_api.send_to_message(msg, agent=True)
