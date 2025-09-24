
import os
import sys
from fastapi.testclient import TestClient
import pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app


client = TestClient(app)

def test_message_endpoint(monkeypatch):
    # Monkeypatch heavy KnowledgeAgent.answer to be fast/fake
    import app.router_agent as ra_mod
    class FakeKnowledge:
        async def answer(self, q): return {'agent':'knowledge','answer':'fake','escalate_to_human':False}
    # Patch instance attribute on RouterAgent
    original_init = ra_mod.RouterAgent.__init__
    def fake_init(self):
        original_init(self)
        self.knowledge = FakeKnowledge()
    monkeypatch.setattr(ra_mod.RouterAgent, "__init__", fake_init)
    # create new client and call endpoint
    r = client.post('/api/message', json={'message':'Quais as taxas da maquininha?','user_id':'client789'})
    assert r.status_code == 200
    j = r.json()
    assert j['ok'] is True
    assert 'agent' in j['result']
