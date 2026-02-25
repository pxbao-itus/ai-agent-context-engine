# 🧠 Context Engine RAG

A high-performance, modular Orchestrator for **Retrieval-Augmented Generation (RAG)** built with **FastAPI** and **LangChain**. 

This engine seamlessly coordinates between vector storage, relational chunk data, and multiple LLM providers to deliver context-aware intelligence.

---

## ✨ Features

- ⛓️ **LangChain LCEL**: Modular chain architecture for easy customization.
- 🤖 **Multi-LLM Support**: Switch between **OpenAI (GPT-4o)**, **Google (Gemini 2.0)**, and **Anthropic (Claude 3)** with a single env variable.
- 🗄️ **Dual-Database Strategy**: 
    - **Qdrant**: High-speed vector search for semantic retrieval.
    - **PostgreSQL (pgvector)**: Reliable storage for full text chunks and metadata.
- ☁️ **S3 Integration**: Ready for raw document fetching.
- 🛠️ **Local Development Stack**: Single-command infrastructure setup via Docker Compose.
- 🔍 **Diagnostic Logging**: Beautiful, color-coded console logs tracking every step from query to completion.

---

## 🚀 Quick Start

### 1. Initialize Infrastructure
Spin up Qdrant, Postgres (pgvector), and MinIO (S3-compatible) locally:
```bash
make deps
```

### 2. Environment Setup
Setup your virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure your `.env` file (see `.env.example` for reference):
```env
LLM_PROVIDER="google" # options: google, openai, anthropic
GOOGLE_API_KEY="your_key"
QDRANT_URL="http://localhost:6333"
POSTGRES_DSN="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
```

### 3. Ingest Data
Populate your database with example data (cloned from the Omnisync repo):
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python scripts/ingest_repo.py
```

### 4. Launch the Engine
```bash
make run
```

---

## 🔗 API Usage

### Query the Engine
**Endpoint**: `POST /api/v1/ask`

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "How does the omnisync engine work?"}'
```

---

## 📊 Observability
The engine provides granular logging to help you understand the RAG pipeline in real-time:

- `[QUERY]`: Incoming user request.
- `[QDRANT]`: Semantic search results count.
- `[POSTGRES]`: Full-text chunk retrieval status.
- `[PROMPT]`: The exact, final context-enriched prompt sent to the LLM.
- `[LLM]`: Generation status and provider info.

---

## 🛠️ Project Structure
- `app/api`: FastAPI routes and request handlers.
- `app/services`: Core RAG orchestrator logic (LCEL).
- `app/tools`: Client integrations for Qdrant, Postgres, and S3.
- `scripts/`: Data ingestion and diagnostic utilities.
