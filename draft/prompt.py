# =============================================================================
# PROMPT ENGINEERING MODULE - RAG Context Integration
# =============================================================================
# 
# PURPOSE: This module handles prompt engineering for our RAG system.
# It combines retrieved context with user questions to create effective prompts
# that guide the LLM to generate accurate, context-based responses.
#
# KEY CONCEPTS:
# 1. Prompt Engineering: Crafting effective instructions for LLMs
# 2. Context Integration: Combining retrieved documents with user queries
# 3. Role-Based Prompting: Assigning specific expertise to the LLM
# 4. Constraint-Based Responses: Limiting LLM to use only provided context
#
# WHY THIS IS CRITICAL FOR RAG:
# - Prevents hallucination by restricting LLM to provided context
# - Ensures answers are based on retrieved documents, not general knowledge
# - Improves accuracy and relevance of responses
# - Provides clear structure for LLM to follow
# Qeustion / proejcts -> RAG -> LLM -> Answer



# =============================================================================
# 
def build_prompt(context_docs, question):
    """
    Build an effective RAG prompt by combining context with the user's question.
    
    This function is the "Augmentation" component of RAG - it takes the retrieved
    documents and combines them with the user's question to create a comprehensive
    prompt that guides the LLM to generate accurate, context-based answers.
    
    PARAMETERS:
        context_docs (list): List of retrieved document texts from vector store
        question (str): The user's original question or query
    
    RETURNS:
        str: A well-structured prompt for the LLM
    
    PROMPT ENGINEERING STRATEGIES USED:
    1. Role Assignment: "You are a real estate expert" - sets context and expertise
    2. Clear Instructions: "Answer ONLY from the context" - prevents hallucination
    3. Fallback Behavior: "If not found, say I don't know" - handles unknown cases
    4. Structured Format: Clear separation of context, question, and answer
    
    WHY THIS STRUCTURE WORKS:
    - Role-based prompting improves response quality and consistency
    - Explicit constraints reduce hallucination and improve reliability
    - Clear formatting helps LLM understand the task structure
    - Fallback instruction handles edge cases gracefully
    """
    # Combine multiple context documents into a single text block
    # Double newline separation creates clear document boundaries
    # This helps the LLM distinguish between different sources
    context = "\n\n".join(context_docs)

    # Build the complete prompt using f-string formatting
    # This structure follows best practices for RAG prompting:
    return f"""
Role: You Guidline eingeer at Toshiba, you shsould answer me about any question realted to the company or its products.

Answer ONLY from the context below.
If not found, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
    
    # PROMPT COMPONENTS EXPLAINED:
    # 
    # 1. ROLE ASSIGNMENT:
    # "You Guidline eingeer at Toshiba, you shsould answer me about any question realted to the company or its products."
    # - Sets the LLM's mindset and expertise level
    # - Improves response quality by providing domain context
    # - Helps generate more professional and accurate answers
    # 
    # 2. CONSTRAINT INSTRUCTIONS:
    # "Answer ONLY from the context below."
    # - Critical for preventing hallucination
    # - Forces LLM to use only provided information
    # - Ensures answers are grounded in retrieved documents
    # 
    # 3. FALLBACK HANDLING:
    # "If not found, say I don't know."
    # - Provides graceful handling when context doesn't contain answer
    # - Prevents LLM from making up information
    # - Maintains honesty and reliability
    # 
    # 4. CONTEXT SECTION:
    # Contains the actual retrieved documents
    # - This is the knowledge base for the LLM
    # - Multiple documents provide comprehensive information
    # - Clear separation helps LLM process each source
    # 
    # 5. QUESTION SECTION:
    # The original user query
    # - Maintains the original intent and focus
    # - Ensures LLM addresses the specific question asked
    # 
    # 6. ANSWER SECTION:
    # Placeholder for LLM response
    # - Signals where the LLM should generate its answer
    # - Provides clear structure for the response


