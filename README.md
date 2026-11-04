# FinAgent MCP - Servidor de Ferramentas Financeiras para Agentes de IA

Este projeto demonstra a implementação de um servidor **MCP (Model Context Protocol)** em Python integrado a uma base de dados SQLite para expor ferramentas seguras de consulta e simulação financeira a Agentes de IA Generativa.

## 🛠️ Tecnologias Utilizadas
- **Python 3.13**
- **MCP SDK** (Protocolo da Anthropic para integração de contexto)
- **SQLite3** (Base de dados relacional para persistência simulada)
- **Asyncio / Stdio** (Comunicação entre processos via entrada/saída padrão)

## 🏗️ Arquitetura do Sistema
1. **`database.py`**: Criação da estrutura de tabelas e população com dados simulados.
2. **`server.py`**: Servidor MCP que expõe ferramentas (`get_account_balance`, `get_recent_transactions`, `simulate_transfer`).
3. **`main.py`**: Cliente/Agente que se liga ao servidor via protocolo Stdio e executa as chamadas de ferramentas de forma segura.

## 🚀 Como Executar
1. Instalar dependências:
   ```bash
   pip install mcp