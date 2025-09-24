
import sqlite3
from typing import Dict, Any
from app.config import DB_PATH
from app.guardrails import check_guardrails

def _get_db_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

# tools
def get_user_profile(user_id: str) -> Dict[str, Any]:
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {"found": False}
    return {"found": True, "user_id": row["user_id"], "name": row["name"], "email": row["email"]}

def get_transactions(user_id: str, limit: int = 10):
    conn = _get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

class SupportAgent:
    def __init__(self):
        pass

    async def handle(self, message: str, user_id: str) -> Dict[str, Any]:
        # guardrails check
        escalate, reason = check_guardrails(message)
        if escalate:
            return {"agent":"support","answer":"Sua pergunta foi identificada como sensível e será encaminhada a um humano.","escalate_to_human": True, "reason": reason}

        profile = get_user_profile(user_id)
        if not profile.get("found"):
            return {"agent":"support","answer":"Não encontrei seu cadastro. Deseja abrir um chamado para suporte humano?","escalate_to_human": True, "reason":"user_not_found"}

        m = message.lower()
        if "transfer" in m or "transferência" in m or "não consigo transfer" in m:
            tx = get_transactions(user_id, limit=5)
            return {"agent":"support","answer": f"Olá {profile['name']}. Encontrei {len(tx)} transações recentes. Ex.: {tx[:3]}","escalate_to_human": False}
        if "login" in m or "entrar" in m or "senha" in m:
            return {"agent":"support","answer": f"Olá {profile['name']}, parece um problema de autenticação. Deseja abrir um ticket para suporte humano?","escalate_to_human": True, "reason":"auth_issue"}

        return {"agent":"support","answer": f"Olá {profile['name']}, não tenho a resposta precisa mas posso abrir um chamado. Mensagem: {message[:200]}","escalate_to_human": False}
