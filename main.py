import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_agent():
    # Configurar os parâmetros para iniciar o servidor MCP em segundo plano
    server_params = StdioServerParameters(
        command=sys.executable,  # Usa o interpretador Python atual
        args=["server.py"]
    )

    print("--- CONECTANDO AO SERVIDOR MCP ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar a sessão do protocolo
            await session.initialize()
            
            # 1. Listar as ferramentas disponibilizadas pelo servidor MCP
            tools_response = await session.list_tools()
            print("\n[Ferramentas MCP Disponíveis]:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            # 2. Simular o Agente a chamar a ferramenta de consulta de saldo
            print("\n[Agente executando]: Consultar saldo do usuário 'usr_123'...")
            balance_result = await session.call_tool("get_account_balance", {"user_id": "usr_123"})
            print(f"Resposta do Servidor MCP: {balance_result.content[0].text}")

            # 3. Simular o Agente a realizar uma simulação de transferência PIX
            print("\n[Agente executando]: Simular transferência de R$ 150.00 para 'Mercado Local'...")
            transfer_result = await session.call_tool(
                "simulate_transfer", 
                {"user_id": "usr_123", "amount": 150.0, "recipient": "Mercado Local"}
            )
            print(f"Resposta do Servidor MCP: {transfer_result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_agent())