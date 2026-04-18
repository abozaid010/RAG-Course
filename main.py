from fastapi import FastAPI
from pydantic import BaseModel

from vector_store import query_projects
from llm import ask_llm
from prompt import build_prompt

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/ask")
async def ask(q: Query):
    docs = query_projects(q.question, k=3)

    prompt = build_prompt(docs, q.question)

    answer = await ask_llm(prompt)

    return {
        "answer": answer,
        "context": docs
    }