import sqlite3
from typing import List, Dict, Any
from mcp.server.mcpserver import MCPServer as FastMCP
from database import DB_PATH, init_db

# Inicializar o servidor MCP com o nome do nosso projeto
mcp = FastMCP("FinAgent Server")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_account_balance(user_id: str) -> str:
    """Retorna o saldo atual da conta do usuário pelo ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"Saldo do usuário {user_id}: R$ {row['balance']:.2f}"
    return f"Usuário {user_id} não encontrado."

@mcp.tool()
def get_recent_transactions(user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Consulta as últimas transações registradas para o usuário."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, amount, description FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@mcp.tool()
def simulate_transfer(user_id: str, amount: float, recipient: str) -> str:
    """Simula o impacto de uma transferência no saldo da conta sem alterar o banco."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"Erro: Usuário {user_id} não encontrado."
    
    current_balance = row['balance']
    if current_balance >= amount:
        new_balance = current_balance - amount
        return (f"Simulação Aprovada! Transferência de R$ {amount:.2f} para {recipient} é possível. "
                f"Saldo atual: R$ {current_balance:.2f} | Saldo final estimado: R$ {new_balance:.2f}")
    else:
        return (f"Simulação Recusada: Saldo insuficiente. "
                f"Saldo atual: R$ {current_balance:.2f} | Valor solicitado: R$ {amount:.2f}")

if __name__ == "__main__":
    init_db()  # Garante que o banco exista antes de subir o servidor
    mcp.run(transport='stdio')