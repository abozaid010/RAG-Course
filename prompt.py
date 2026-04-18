def build_prompt(context_docs, question):
    context = "\n\n".join(context_docs)

    return f"""
You are a real estate expert.

Answer ONLY from the context below.
If not found, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""