# =============================================================================
# MAIN APPLICATION - FastAPI RAG System
# =============================================================================
# 
# PURPOSE: This is the main entry point for our RAG (Retrieval-Augmented Generation)
# system. It provides a REST API endpoint that orchestrates the complete RAG workflow.
#
# RAG WORKFLOW OVERVIEW:
# 1. User submits a question via API
# 2. System retrieves relevant documents using vector search
# 3. Retrieved context is combined with the question in a prompt
# 4. LLM generates an answer based on the provided context
# 5. Response includes both the answer and the retrieved context
#
# KEY COMPONENTS:
# - FastAPI: Modern, fast web framework for building APIs
# - Pydantic: Data validation and serialization
# - Async/await: Non-blocking operations for better performance
#
# WHY THIS ARCHITECTURE:
# - Scalable: Can handle multiple concurrent requests
# - Standard: REST API is widely understood and supported
# - Modular: Each component has a single responsibility
# - Testable: Clean separation makes testing easier
# =============================================================================

from fastapi import FastAPI  # Modern, high-performance web framework
from pydantic import BaseModel  # Data validation and settings management

# Import our RAG system components
from vector_store import query_projects  # Vector database retrieval
from deep_seek_llm import ask_llm       # LLM integration
from prompt import build_prompt         # Prompt engineering

# Initialize FastAPI application
# FastAPI provides automatic API documentation, validation, and serialization
# It's built on Starlette for the web parts and Pydantic for the data parts
app = FastAPI(
    title="RAG Real Estate Assistant",
    description="A Retrieval-Augmented Generation system for real estate queries",
    version="1.0.0"
)


# Define the request data model using Pydantic
# This provides automatic validation and serialization
# FastAPI will automatically validate incoming requests against this model
class Query(BaseModel):
    """
    Request model for user questions.
    
    Pydantic models provide:
    - Automatic data validation
    - Type conversion and checking
    - API documentation generation
    - Serialization/deserialization
    """
    question: str  # The user's question or query
    
    # Pydantic automatically validates that 'question' is a string
    # If validation fails, FastAPI returns a 422 Unprocessable Entity error

# L
# Define the main API endpoint for RAG queries
# @app.post decorator creates a POST endpoint at /ask
# FastAPI automatically handles request parsing and response serialization
@app.post("/ask")
async def ask(q: Query):
    """
    Main RAG endpoint that processes user questions and returns AI-generated answers.
    
    This function orchestrates the complete RAG workflow:
    1. Retrieval: Find relevant documents using vector search
    2. Augmentation: Combine context with the user's question
    3. Generation: Generate answer using LLM
    4. Response: Return both answer and context
    
    PARAMETERS:
        q (Query): Pydantic model containing the user's question
    
    RETURNS:
        dict: Contains the generated answer and the retrieved context documents
    
    WHY ASYNC:
    - Non-blocking: Doesn't freeze the server while waiting for LLM response
    - Scalability: Can handle multiple concurrent requests efficiently
    - Performance: Better resource utilization under load
    1, 2, 3..
    RAG WORKFLOW STEPS:
    """
    
    # STEP 1: RETRIEVAL
    # Query the vector database to find the most relevant documents
    # This is the "R" in RAG - Retrieval
    # k=3 means we want the top 3 most relevant documents
    # json_data = """
    
    # """
    # pdf = ""    ""
    

    # vector_Db = ""


    docs = query_projects(q.question, k=3)

    # WHY VECTOR SEARCH:
    # - Finds semantically similar documents, not just keyword matches
    # - Handles synonyms and related concepts
    # - Provides better context for the LLM
    # - Scales efficiently to large document collections

    # STEP 2: AUGMENTATION
    # Build the prompt by combining retrieved context with the user's question
    # This is the "A" in RAG - Augmentation
    # The prompt engineering ensures the LLM uses only the provided context
    prompt = build_prompt(docs, q.question)
    
    # WHY PROMPT ENGINEERING:
    # - Prevents hallucination by constraining LLM to context
    # - Provides clear instructions for consistent responses
    # - Handles edge cases when context doesn't contain answer
    # - Sets appropriate role and expertise level

    # STEP 3: GENERATION
    # Send the prompt to the LLM and get the response
    # This is the "G" in RAG - Generation
    # The LLM generates an answer based on the provided context
    answer = await ask_llm(prompt)
    
    # WHY LLM GENERATION:
    # - Understands natural language and context
    # - Can synthesize information from multiple documents
    # - Provides human-like responses
    # - Handles complex reasoning and inference

    # STEP 4: RESPONSE
    # Return both the answer and the context for transparency
    # Including context allows users to verify the answer's source
    return {
        "answer": answer,    # The LLM-generated response
        "context": docs      # The retrieved documents used as context
    }
    
    # RESPONSE STRUCTURE BENEFITS:
    # - Transparency: Users can see the source information
    # - Debugging: Easy to verify why certain answers were generated
    # - Trust: Builds confidence in the system's responses
    # - Flexibility: Frontend can display both answer and sources

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


