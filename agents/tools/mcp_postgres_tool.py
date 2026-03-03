import asyncio
import json
import os

from langchain.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _run_postgres_query_async(query: str) -> str:
    db_uri = os.environ.get("DATABASE_URI")
    if not db_uri:
        return json.dumps(
            {"error": "A variável de ambiente DATABASE_URI não está definida."}
        )

    env = os.environ.copy()

    server_params = StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "DATABASE_URI",
            "crystaldba/postgres-mcp",
            "--access-mode=unrestricted",
        ],
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("execute_sql", arguments={"query": query})

            output = []
            for item in result.content:
                if item.type == "text":
                    output.append(item.text)
                else:
                    output.append(str(item))

            return json.dumps(output, ensure_ascii=False)


def _run_postgres_query(query: str) -> str:
    try:
        return asyncio.run(_run_postgres_query_async(query))
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool(
    "mcp_postgres_tool",
    description="Use esta ferramenta MCP para consultar o banco de dados PostgreSQL. Forneça a consulta SQL completa como entrada.",
)
def get_mcp_postgres_tool(query: str) -> str:
    """Ferramenta MCP para consultar o PostgreSQL utilizando o postgres-mcp da crystaldba."""
    return _run_postgres_query(query)
