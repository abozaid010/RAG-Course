# RAG Agent Backend (DeepSeek)

A minimal, production-ready RAG agent using DeepSeek for LLM and FastEmbed for local embeddings.

## 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env and add your DEEPSEEK_API_KEY
```

## 2. Ingest Data

Run the ingestor to populate the vector database from `test_data.json`:

```bash
python app/ingestor.py
```

## 3. Run API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

## 4. Usage

Send a chat request:

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "user-123",
           "message": "What projects do you have in New Cairo?"
         }'
```
