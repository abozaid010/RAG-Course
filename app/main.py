from fastapi import FastAPI
from app.models import ChatRequest, ChatResponse
from app.agent import agent_service

app = FastAPI(title="RAG Agent Backend")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = agent_service.chat(request.session_id, request.message)
    return ChatResponse(reply=reply)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
