import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase

load_dotenv()


@tool(
    "postgres_tool",
    description="Use esta ferramenta para consultar o banco de dados PostgreSQL. Forneça a consulta SQL completa como entrada.",
)
def get_postgres_tool(query: str) -> str:
    db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"))
    sql_tool = QuerySQLDataBaseTool(db=db, verbose=True)
    return sql_tool.run(query)
