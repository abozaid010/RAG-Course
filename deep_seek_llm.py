import httpx
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")

async def ask_llm(prompt: str):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=data)
        return res.json()["choices"][0]["message"]["content"]