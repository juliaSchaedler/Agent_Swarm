
class CustomAgent:
    def __init__(self):
        pass

    async def handle(self, message: str, user_id: str) -> dict:
        if "notícias" in message.lower() or "news" in message.lower():
            return {"agent":"custom","answer":"Posso integrar com um provedor de notícias (bônus).","escalate_to_human": False}
        return {"agent":"custom","answer": f"Agente custom processou: {message}","escalate_to_human": False}
