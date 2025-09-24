
from fastapi import FastAPI
from pydantic import BaseModel
from app.router_agent import RouterAgent

app = FastAPI(title="Agent Swarm API")
router_agent = RouterAgent()

class MessageIn(BaseModel):
    message: str
    user_id: str

@app.post('/api/message')
async def process_message(payload: MessageIn):
    result = await router_agent.handle(payload.message, payload.user_id)
    return {"ok": True, "result": result}
