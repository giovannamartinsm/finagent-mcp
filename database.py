import sqlite3

DB_PATH = "finance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Criar tabela de contas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        user_id TEXT PRIMARY KEY,
        balance REAL NOT NULL
    )
    """)
    
    # Criar tabela de transações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        category TEXT,
        amount REAL,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES accounts(user_id)
    )
    """)
    
    # Inserir dados fictícios se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO accounts VALUES ('usr_123', 2500.50)")
        cursor.executemany("INSERT INTO transactions (user_id, category, amount, description) VALUES (?, ?, ?, ?)", [
            ('usr_123', 'Alimentação', -45.90, 'Supermercado'),
            ('usr_123', 'Transporte', -15.00, 'Uber'),
            ('usr_123', 'Salário', 3000.00, 'Depósito Empresa'),
            ('usr_123', 'Lazer', -120.00, 'Restaurante')
        ])
        conn.commit()
    
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados SQLite inicializado com sucesso!")