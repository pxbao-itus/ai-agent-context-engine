# Context Engine RAG with LangChain

This project is a simple orchestrator for Retrieval-Augmented Generation (RAG). It receives user queries, coordinates between Qdrant (VectorDB), Postgres (chunk storage), AWS S3 (raw file storage), and Anthropic Claude (LLM) using the LangChain framework to produce answers based on retrieved context.

## Prerequisites
- Python 3.10+
- Access to an Anthropic API Key
- Access to AWS S3, Postgres, and Qdrant instances.

## Setup
1. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` (you can create one) and override the keys, or export the following variables in your environment:
   ```bash
   ANTHROPIC_API_KEY="your-key-here"
   QDRANT_URL="http://localhost:6333"
   POSTGRES_DSN="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
   AWS_ACCESS_KEY_ID="your-aws-access-key"
   AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
   S3_BUCKET_NAME="your-bucket-name"
   ```

## Running the Application
```bash
uvicorn app.main:app --reload
```

## Testing the Pipeline
Once the server is running, you can send POST requests to the `/api/v1/ask` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}'
```

_Note that this base structure includes some mock classes (like embeddings) that you should replace with your actual embedding models once your pipelines are fully connected._
