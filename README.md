# RAG System Tutorial - ChromaDB + DeepSeek LLM

## 🎯 Class 1: Building a Complete RAG System

Welcome to this comprehensive tutorial on building a **Retrieval-Augmented Generation (RAG)** system using **ChromaDB** and **DeepSeek LLM**. This project demonstrates how to create an intelligent real estate assistant that can answer questions based on a knowledge base of property information.

### 📚 What You'll Learn

1. **RAG Architecture**: Understanding the complete RAG workflow
2. **Vector Databases**: How ChromaDB enables semantic search
3. **Embeddings**: Converting text to numerical vectors
4. **LLM Integration**: Connecting with DeepSeek's API
5. **Prompt Engineering**: Crafting effective RAG prompts
6. **API Development**: Building a FastAPI REST service
7. **Data Ingestion**: Loading and processing real estate data

---

## 🏗️ System Architecture

### RAG Workflow Overview

```
User Question → Vector Search → Context Retrieval → Prompt Building → LLM Generation → Response
     ↓              ↓                ↓                ↓               ↓            ↓
  "What are     ChromaDB finds    Relevant docs    Context +      DeepSeek     AI Answer
 affordable    similar projects   combined with    question       generates    based on
 apartments?"   using embeddings  in structured   is sent to     response     provided
                 semantic search   prompt format   API            using only   context
```

### Core Components

1. **Retrieval**: ChromaDB vector database finds relevant documents
2. **Augmentation**: Retrieved context is combined with user question
3. **Generation**: DeepSeek LLM generates answer based on context

---

## 📁 Project Structure

```
RAG-Course/
├── main.py              # FastAPI application and RAG orchestration
├── vector_store.py      # ChromaDB integration and vector operations
├── deep_seek_llm.py     # DeepSeek API integration
├── prompt.py           # Prompt engineering for RAG
├── load_data.py        # Data ingestion script
├── requirements.txt    # Python dependencies
├── data_sample.json    # Sample real estate data
└── README.md          # This tutorial file
```

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Set your DeepSeek API key
export DEEPSEEK_API_KEY="your_api_key_here"

# Or create a .env file:
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

### 3. Load Data into Vector Database

```bash
# This will load real estate data into ChromaDB
python load_data.py
```

### 4. Start the API Server

```bash
# Start FastAPI server with auto-reload
uvicorn main:app --reload

# Server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### 5. Test the System

```bash
# Test with curl
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are some affordable apartments in Riyadh?"}'
```

---

## 📖 Detailed Component Guide

### 1. Vector Store (`vector_store.py`)

**Purpose**: Handles document storage and retrieval using ChromaDB.

**Key Concepts**:
- **Embeddings**: Text converted to 384-dimensional vectors
- **Similarity Search**: Finding documents closest to query in vector space
- **Metadata**: Structured data for filtering and display

**Why ChromaDB**:
- Open-source and free
- Optimized for AI applications
- Easy integration with sentence-transformers
- Built-in indexing for fast search

### 2. LLM Integration (`deep_seek_llm.py`)

**Purpose**: Communicates with DeepSeek's API for text generation.

**Key Features**:
- Async HTTP requests for better performance
- Error handling and retry logic
- Temperature control for response consistency
- OpenAI-compatible API format

**Why DeepSeek**:
- Cost-effective alternative to OpenAI
- High-quality responses
- Good multilingual support
- Compatible API format

### 3. Prompt Engineering (`prompt.py`)

**Purpose**: Creates effective prompts that guide LLM responses.

**RAG Prompt Strategies**:
- **Role Assignment**: "You are a real estate expert"
- **Context Constraints**: "Answer ONLY from the context below"
- **Fallback Handling**: "If not found, say I don't know"
- **Structured Format**: Clear separation of components

### 4. API Server (`main.py`)

**Purpose**: Provides REST API interface for the RAG system.

**FastAPI Benefits**:
- Automatic API documentation
- Request validation with Pydantic
- Async support for better performance
- Built-in serialization

### 5. Data Ingestion (`load_data.py`)

**Purpose**: Loads real estate data into the vector database.

**Process Flow**:
1. Read JSON data from file
2. Extract project information
3. Create text documents for embedding
4. Generate embeddings and store in ChromaDB

---

## 🔍 How RAG Works: Step-by-Step

### Step 1: User Query
```
Input: "What are some affordable apartments in Riyadh?"
```

### Step 2: Vector Search
- Query is converted to embedding vector
- ChromaDB finds similar documents using cosine similarity
- Returns top 3 most relevant project documents

### Step 3: Context Building
```
Context:
Project: Al Riyadh Residences
City: Riyadh
Start Price: 250,000 SAR
Description: Modern apartments with affordable pricing...

Project: Riyadh Gardens
City: Riyadh  
Start Price: 180,000 SAR
Description: Budget-friendly residential complex...
```

### Step 4: Prompt Creation
```
You are a real estate expert.
Answer ONLY from the context below.
If not found, say "I don't know".

Context: [retrieved documents]
Question: What are some affordable apartments in Riyadh?
Answer:
```

### Step 5: LLM Generation
DeepSeek processes the prompt and generates:
```
Based on the provided context, there are two affordable apartment options in Riyadh:

1. Al Riyadh Residences - Starting at 250,000 SAR, offering modern apartments with affordable pricing
2. Riyadh Gardens - Starting at 180,000 SAR, described as a budget-friendly residential complex
```

---

## 🧪 Testing and Examples

### Example Queries

1. **Price-based queries**:
   ```json
   {"question": "What properties are under 300,000 SAR?"}
   ```

2. **Location-based queries**:
   ```json
   {"question": "Show me projects in Jeddah"}
   ```

3. **Property type queries**:
   ```json
   {"question": "Are there any villas available?"}
   ```

4. **Developer queries**:
   ```json
   {"question": "What projects does Dar Al Arkan have?"}
   ```

### Expected Response Format

```json
{
  "answer": "Based on the provided context...",
  "context": [
    "Project: Example Project\nCity: Riyadh\n...",
    "Project: Another Project\nCity: Riyadh\n..."
  ]
}
```

---

## 🛠️ Advanced Topics

### Scaling Considerations

1. **Vector Database Scaling**:
   - Use ChromaDB Server for production
   - Consider sharding for large datasets
   - Implement caching for frequent queries

2. **LLM Optimization**:
   - Implement response caching
   - Use batch processing for multiple queries
   - Consider model fine-tuning for domain-specific tasks

3. **Performance Monitoring**:
   - Track query latency
   - Monitor embedding generation time
   - Log API response times and errors

### Security Best Practices

1. **API Security**:
   - Never hardcode API keys
   - Use environment variables for configuration
   - Implement rate limiting
   - Add authentication for production use

2. **Data Privacy**:
   - Sanitize input data
   - Implement data retention policies
   - Consider encryption for sensitive data

---

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **API Key Issues**:
   ```bash
   # Check environment variable is set
   echo $DEEPSEEK_API_KEY
   ```

3. **ChromaDB Issues**:
   ```bash
   # Clear vector database if needed
   # Delete the chroma_storage directory
   ```

4. **Memory Issues**:
   - Process data in smaller batches
   - Monitor memory usage during embedding generation
   - Consider using GPU for embedding generation

### Debug Mode

Add logging to monitor the RAG workflow:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

---

## 📚 Further Learning

### Next Steps

1. **Enhanced Retrieval**:
   - Implement hybrid search (keyword + semantic)
   - Add query expansion techniques
   - Use re-ranking models

2. **Advanced Prompting**:
   - Implement few-shot examples
   - Add chain-of-thought prompting
   - Use structured output formats

3. **Production Deployment**:
   - Containerize with Docker
   - Set up monitoring and logging
   - Implement CI/CD pipeline

### Related Technologies

- **Alternative Vector DBs**: Pinecone, Weaviate, Milvus
- **Other LLMs**: OpenAI GPT, Anthropic Claude, Llama
- **Embedding Models**: OpenAI embeddings, Cohere, E5
- **Frameworks**: LangChain, LlamaIndex, Haystack

---

## 🤝 Contributing

This tutorial is designed for educational purposes. Feel free to:

- Experiment with different embedding models
- Try different LLM providers
- Implement additional features
- Share improvements and suggestions

---

## 📄 License

This educational project is open source and available for learning purposes.

---

## 🎓 Summary

In this tutorial, you've learned how to build a complete RAG system that:

✅ **Retrieves** relevant documents using vector similarity search  
✅ **Augments** user queries with contextual information  
✅ **Generates** accurate responses using DeepSeek LLM  
✅ **Serves** responses through a modern FastAPI interface  
✅ **Processes** real estate data efficiently  

The key takeaway is that RAG systems combine the strengths of both retrieval systems and language models to provide accurate, context-aware responses that are grounded in actual data rather than just the model's training knowledge.

This architecture can be adapted for any domain - customer support, document analysis, research assistance, and more. The principles remain the same: retrieve relevant context, augment the query, and generate informed responses.
