
from typing import List
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from app.config import RAG_DB
import torch

class KnowledgeAgent:
    def __init__(self, persist_directory: str = str(RAG_DB)):
        # embeddings model
        self.embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embed_model = SentenceTransformer(self.embed_model_name)
        # chroma client
        self.client = PersistentClient(path=persist_directory)
        try:
            self.collection = self.client.get_collection("infinitepay")
        except Exception:
            self.collection = None
        # generator model (Flan-T5 small)
        self.gen_model_name = "google/flan-t5-small"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.gen_model_name)
        self.gen_model = AutoModelForSeq2SeqLM.from_pretrained(self.gen_model_name).to(self.device)

    def similarity_search(self, query: str, k: int = 4) -> List[dict]:
        if self.collection is None:
            return []
        q_emb = self.embed_model.encode([query], convert_to_numpy=True)[0].tolist()
        res = self.collection.query(query_embeddings=[q_emb], n_results=k, include=["documents", "metadatas", "distances"])
        docs = []
        for d, m in zip(res["documents"][0], res["metadatas"][0]):
            docs.append({"text": d, "meta": m})
        return docs

    def _generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        tok = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(self.device)
        outputs = self.gen_model.generate(**tok, max_new_tokens=max_new_tokens)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer

    def answer_question(self, question: str) -> str:
        docs = self.similarity_search(question, k=4)
        context = "\n\n".join([d['text'] for d in docs]) if docs else ""
        prompt = f"Use the context to answer the question concisely. If unsure, say you don't know and suggest contacting support.\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:\n"
        answer = self._generate(prompt)
        # provenance
        prov = ", ".join([m.get('source','unknown') for m in [d['meta'] for d in docs]]) if docs else "none"
        return answer + "\n\nProvenance: " + prov

    # Async wrapper for API
    async def answer(self, question: str) -> dict:
        ans = self.answer_question(question)
        return {"agent": "knowledge", "answer": ans, "escalate_to_human": False}
