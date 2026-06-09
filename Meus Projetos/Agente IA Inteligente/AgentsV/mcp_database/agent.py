import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:5000/sse")

root_agent = Agent(
    name="mcp_database",
    model="gemini-2.0-flash",
    instruction="""Voce e um auditor senior de inteligencia de negocios.
    Responda sempre em portugues do Brasil.
    Use as ferramentas disponiveis para consultar dados reais do banco de dados.
    Ao responder, seja claro, objetivo e formate os dados de forma legivel.
    Nunca invente dados - consulte sempre o banco antes de responder.""",
    tools=[
        MCPToolset(
            connection_params=SseConnectionParams(
                url=MCP_SERVER_URL
            )
        )
    ]
)