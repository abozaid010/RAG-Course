# Simple RAG Tutorial - JSON vs Vector Database Comparison
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

from vector_store import query_projects, query_projects_json
from deep_seek_llm import ask_llm
from prompt import build_prompt

app = FastAPI(title="RAG Tutorial", description="Simple RAG system comparing JSON vs Vector DB")

class Query(BaseModel):
    question: str
    method: str = "vector"  # "json" or "vector"

def json_search(query: str, k: int = 3):
    """Simple JSON keyword search example"""
    data_file = os.path.join(os.path.dirname(__file__), 'realestate_data_sample.json')
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return ["Error: Could not load data file"]
    
    projects = data.get('projects', [])
    results = []
    
    # Simple keyword matching
    query_lower = query.lower()
    for project in projects[:k]:  # Just take first k for simplicity
        text = f"{project.get('en_name', '')} {project.get('description', '')} {project.get('city', '')}"
        if query_lower in text.lower():
            results.append(f"Project: {project.get('en_name', '')}\nLocation: {project.get('city', '')}\nDescription: {project.get('description', '')[:100]}...")
    
    if not results:
        results = ["No matching projects found with keyword search"]
    
    return results

def vector_search(query: str, k: int = 3):
    """Vector database semantic search example"""
    return query_projects(query, k=k)

@app.post("/ask")
async def ask(q: Query):
    """Single endpoint demonstrating both JSON and Vector DB approaches"""
    
    if q.method == "json":
        # Example 1: Simple JSON keyword search
        docs = json_search(q.question, k=3)
        method_used = "JSON Keyword Search"
    else:
        # Example 2: Vector database semantic search
        docs = vector_search(q.question, k=3)
        method_used = "Vector Database Search"
    
    # Generate answer using LLM
    prompt = build_prompt(docs, q.question)
    answer = await ask_llm(prompt)
    
    return {
        "answer": answer,
        "method_used": method_used,
        "context": docs,
        "comparison": {
            "json_search": "Fast keyword matching, limited to exact words",
            "vector_search": "Semantic understanding, finds related concepts"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


