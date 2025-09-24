# Agent Swarm

Agent Swarm is a modular application that demonstrates the orchestration of multiple AI agents collaborating to perform tasks. The project uses an open-source architecture, replacing paid services like OpenAI with alternatives such as [Ollama](https://ollama.ai/) and [ChromaDB](https://www.trychroma.com/).

---

## 📌 Features

- 🤖 Multi-agent orchestration (Router Agent, Knowledge Agent, etc.)
- 🔍 Vector database using **ChromaDB** (local embeddings storage and search)
- 🧠 LLM integration using **Ollama** (open-source models like `llama2`, `mistral`, etc.)
- 🧪 Unit and integration tests with **pytest**
- 🐳 Easy to run locally with **virtualenv** or **Docker**

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** (web server)
- **ChromaDB** (vector database)
- **Ollama** (LLM inference engine)
- **Pytest** (testing)
- **Docker** (optional, for containerized execution)

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/agent-swarm.git
cd agent-swarm
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and run Ollama
Follow [Ollama installation guide](https://ollama.ai/download) for your OS.  
Example:
```bash
ollama run llama2
```

### 5. Run ChromaDB (persistent database)
No external setup required — ChromaDB runs locally as part of the app.

---

## 🚀 Usage

### Start the application
```bash
uvicorn app.main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

### Example request
```bash
curl -X POST "http://127.0.0.1:8000/query"      -H "Content-Type: application/json"      -d '{"question": "What is Agent Swarm?"}'
```

---

## 🧪 Running Tests

Run unit and integration tests with:
```bash
pytest -q tests
```

---

## 🐳 Docker Setup (Optional)

### Build the image
```bash
docker build -t agent-swarm .
```

### Run the container
```bash
docker run -p 8000:8000 agent-swarm
```

---

## 📂 Project Structure

```
agent-swarm/
│── app/
│   ├── main.py          # App entrypoint
│   ├── router_agent.py  # Router Agent
│   ├── knowledge_agent.py # Knowledge Agent (ChromaDB + Ollama)
│── tests/
│   ├── test_unit.py     # Unit tests
│   ├── test_integration.py # Integration tests
│── requirements.txt
│── Dockerfile
│── README.md
```




