
import sqlite3
from pathlib import Path
DB_FILE = Path('db/demo_users.sqlite')
DB_FILE.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
  user_id TEXT PRIMARY KEY,
  name TEXT,
  email TEXT
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  amount REAL,
  description TEXT,
  created_at TEXT
)''')
# demo data
cur.execute("INSERT OR REPLACE INTO users (user_id,name,email) VALUES ('client789','João Silva','joao@example.com')")
cur.execute("INSERT INTO transactions (user_id,amount,description,created_at) VALUES ('client789', 150.0, 'Venda Cartão', '2025-09-01')")
cur.execute("INSERT INTO transactions (user_id,amount,description,created_at) VALUES ('client789', 250.5, 'Recebimento PIX', '2025-09-05')")
conn.commit()
conn.close()
print('DB initialized at', DB_FILE)
