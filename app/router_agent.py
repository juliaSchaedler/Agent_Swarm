
from typing import Dict, Any
from app.knowledge_agent import KnowledgeAgent
from app.support_agent import SupportAgent
from app.custom_agent import CustomAgent
from app.guardrails import check_guardrails

class RouterAgent:
    def __init__(self):
        self.knowledge = KnowledgeAgent()
        self.support = SupportAgent()
        self.custom = CustomAgent()

    def decide(self, message: str) -> str:
        m = message.lower()
        if any(tok in m for tok in ["taxa", "maquininha", "quanto custa", "tarifa", "tarifas", "receba", "pix", "cartão"]):
            return "knowledge"
        if any(tok in m for tok in ["login", "entrar", "transfer", "transferência", "não consigo", "senha", "erro"]):
            return "support"
        return "knowledge"

    async def handle(self, message: str, user_id: str) -> Dict[str, Any]:
        # guardrails first
        escalate, reason = check_guardrails(message)
        if escalate:
            return {"agent":"guardrails","answer":"Pergunta sensível detectada. Encaminhando para humano.","escalate_to_human": True, "reason": reason}

        route = self.decide(message)
        if route == "knowledge":
            return await self.knowledge.answer(message)
        elif route == "support":
            return await self.support.handle(message, user_id)
        else:
            return await self.custom.handle(message, user_id)
