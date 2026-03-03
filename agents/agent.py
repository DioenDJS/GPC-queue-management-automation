from pathlib import Path

from langchain.agents import create_agent

from helpers.llms import LLMProvider, Llms

base_dir = Path(__file__).resolve().parent


def call_agent(query: str):
    main_agent = create_agent(
        model=Llms(provider=LLMProvider.OLLAMA_GLM_5_CLOUD).get_llm(),
        tools=[],
        system_prompt=(base_dir / "config" / "system_prompt.yaml").read_text(),
    )
    result = main_agent.invoke({"messages": [{"role": "user", "content": query}]})

    print(result)
