# =============================================================================
# VECTOR STORE MODULE - ChromaDB Integration for RAG System
# =============================================================================
# 
# PURPOSE: This module handles the vector database operations for our RAG system.
# It manages document storage, retrieval, and similarity search using ChromaDB.
#
# KEY CONCEPTS:
# 1. Vector Database: Stores documents as numerical embeddings for fast similarity search
# 2. Embeddings: Text converted to numerical vectors that capture semantic meaning
# 3. Similarity Search: Finding documents most relevant to a query using vector distance
# 4. ChromaDB: Open-source vector database optimized for AI applications
# meta_data: ex
# WHY WE NEED THIS:
# - Traditional keyword search is limited - it can't understand semantic meaning
# - Vector search finds conceptually similar documents, not just keyword matches
# - Enables RAG by providing relevant context to the LLM for accurate responses
# - Scales to thousands of documents with fast retrieval times
# =============================================================================

import chromadb  # Vector database for storing and querying document embeddings
from sentence_transformers import SentenceTransformer  # Pre-trained model for text embeddings

# Initialize ChromaDB client with persistent storage
# ChromaDB is a vector database that stores embeddings and enables fast similarity search
# It handles the heavy lifting of vector operations, indexing, and retrieval
# Using persistent storage ensures data is saved between sessions
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection named "projects"
# Collections are like tables in traditional databases - they group related documents
# get_or_create_collection will return existing collection or create new one
# This ensures we don't lose data if the script runs multiple times
collection = client.get_or_create_collection(
    name="projects"  # Collection name for storing real estate project documents
)


# This ensures we don't lose data if the script runs multiple times
device_collection = client.get_or_create_collection(
    name="devices"  # Collection name for storing device information
)
# Initialize the sentence transformer model
# all-MiniLM-L6-v2 is a lightweight, fast model that converts text to 384-dimensional vectors
# It's trained on large datasets and provides good balance between speed and quality
# MiniLM models are distilled versions of larger models, making them efficient for production
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(texts):
    """
    Convert text documents to numerical embeddings.
    
    PARAMETERS:
        texts (list): List of text strings to be converted to embeddings
    
    RETURNS:
        list: List of embedding vectors (each vector is a list of floats)
    
    WHY THIS FUNCTION IS CRITICAL:
    - Converts human-readable text to machine-understandable numerical format
    - Enables semantic similarity comparison between documents
    - Each embedding captures the meaning/semantic content of the text
    - Similar texts will have similar embedding vectors (close in vector space)
    
    TECHNICAL DETAILS:
    - all-MiniLM-L6-v2 produces 384-dimensional vectors
    - The model uses attention mechanisms to understand text context
    - .encode() handles tokenization and model inference automatically
    - .tolist() converts numpy arrays to Python lists for ChromaDB compatibility
    """
    return model.encode(texts).tolist()


def add_projects(projects):
    """
    Add real estate project documents to the vector database.
    
    This function processes raw project data and stores it in ChromaDB with embeddings.
    It's the data ingestion pipeline for our RAG system.
    
    PARAMETERS:
        projects (list): List of project dictionaries containing real estate data
    
    PROCESS FLOW:
    1. Extract and format text content from each project
    2. Create structured metadata for filtering and retrieval
    3. Generate unique IDs for each document
    4. Convert text to embeddings using the sentence transformer
    5. Store everything in ChromaDB for fast retrieval
    
    WHY THIS STRUCTURE:
    - Documents: Full text content for semantic search and LLM context
    - Metadata: Structured data for filtering (city, price, etc.)
    - IDs: Unique identifiers for document management
    - Embeddings: Numerical representations for similarity search
    """
    documents = []     # Store the full text content of each project
    metadatas = []     # Store structured metadata for filtering
    ids = []           # Store unique identifiers for each document

    # Process each project and prepare it for vector storage
    for p in projects:
        # Create a comprehensive text document that combines all project information
        # This rich text will be used for semantic search and as context for the LLM
        text = f"""
        Project: {p.get('en_name')}
        Arabic Name: {p.get('ar_name')}
        City: {p.get('city')}
        District: {p.get('district')}
        Developer: {p.get('developer_name')}
        Types: {p.get('properties_types')}
        Start Price: {p.get('start_price')}
        Description: {p.get('description')}
        """

        documents.append(text)

        # Create metadata for structured filtering and retrieval
        # Metadata allows us to filter results by specific criteria
        # It's also useful for displaying search results to users
        metadatas.append({
            "id": p.get("id"),                    # Unique project identifier
            "city": p.get("city"),                # City for geographic filtering
            "price": p.get("start_price"),        # Price range filtering
            "types": ",".join(p.get("properties_types", []))  # Property types as string
        })

        # Use the project ID as the document ID
        # This ensures we can reference and update specific documents
        ids.append(p.get("id"))

    # Generate embeddings for all documents at once
    # Batch processing is more efficient than processing one by one
    embeddings = embed(documents)

    # Add everything to ChromaDB
    # ChromaDB will automatically index the embeddings for fast similarity search
    collection.add(
        documents=documents,      # Full text content for context
        metadatas=metadatas,      # Structured metadata for filtering
        ids=ids,                  # Unique identifiers
        embeddings=embeddings     # Pre-computed embeddings for faster insertion
    )


def query_projects(query, k=3):
    """
    Find most relevant projects for a given query using semantic search.
    
    This is the core retrieval function in our RAG system.
    It finds documents that are semantically similar to the user's query.
    
    PARAMETERS:
        query (str): User's question or search query
        k (int): Number of most relevant documents to return (default: 3)
    
    RETURNS:
        list: List of the most relevant document texts
    
    HOW IT WORKS:
    1. Convert the user's query to an embedding vector
    2. Search ChromaDB for documents with similar embeddings
    3. Return the top k most relevant documents
    
    WHY SEMANTIC SEARCH:
    - Understands meaning, not just keywords
    - Finds relevant documents even if they don't contain exact query terms
    - Provides better context for the LLM to generate accurate answers
    - Handles synonyms and related concepts automatically
    
    EXAMPLE:
    Query: "affordable apartments in Riyadh"
    Results: Documents about low-cost housing in Riyadh, even if they don't contain "affordable"
    """
    # Convert the user's query to an embedding
    # We wrap query in a list because embed() expects a list of texts
    # [0] extracts the single embedding from the returned list
    query_embedding = embed([query])[0]

    # Search ChromaDB for similar documents
    # ChromaDB uses efficient vector search algorithms (like HNSW) to find nearest neighbors
    results = collection.query(
        query_embeddings=[query_embedding],  # The query embedding to search for
        n_results=k                          # Number of most similar documents to return
    )

    # Return the document texts (not metadata or embeddings)
    # These documents will be used as context for the LLM
    return results["documents"][0]





def query_projects_json(query, k=3):
    """
    Find most relevant real estate projects from realestate_data_sample.json using semantic search.
    
    This function is specifically designed to work with the real estate project data
    structure from realestate_data_sample.json, which contains detailed property information
    including locations, prices, developers, and property types.
    
    PARAMETERS:
        query (str): User's question about real estate projects
        k (int): Number of most relevant projects to return (default: 3)
    
    RETURNS:
        list: List of formatted project information as context for LLM
    
    HOW IT WORKS:
    1. Load real estate projects from realestate_data_sample.json
    2. Create searchable text content from each project
    3. Convert to embeddings and search for semantic similarity
    4. Return formatted project information
    
    DATA STRUCTURE HANDLED:
    - Project names (ar_name, en_name)
    - Descriptions and locations
    - Property types (commercial, residential, medical, etc.)
    - Pricing information and payment plans
    - Developer information
    - City and district information
    """
    import json
    import os
    
    # Load the real estate data
    data_file = os.path.join(os.path.dirname(__file__), 'realestate_data_sample.json')
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return ["Error: realestate_data_sample.json file not found"]
    except json.JSONDecodeError:
        return ["Error: Invalid JSON format in realestate_data_sample.json"]
    
    projects = data.get('projects', [])
    if not projects:
        return ["No projects found in realestate_data_sample.json"]
    
    # Create searchable documents from project data
    documents = []
    metadatas = []
    ids = []
    
    for i, project in enumerate(projects):
        # Create comprehensive text content for each project
        project_text = f"""
        Project Name: {project.get('en_name', '')} - {project.get('ar_name', '')}
        Developer: {project.get('developer_name', '')}
        Location: {project.get('city', '')} - {project.get('district', '')} - {project.get('country', '')}
        Description: {project.get('description', '')}
        Property Types: {', '.join(project.get('properties_types', []))}
        Start Price: {project.get('start_price', 0):,}
        Area: {project.get('area', 0)} sqm
        Units Count: {project.get('units_count', 0)}
        Gated Community: {project.get('gated', False)}
        Finishing Type: {', '.join(project.get('finishing_type', []))}
        Delivery Date: {project.get('delivery_date', 0)} years
        Location Landmark: {project.get('location_landmark', '')}
        """.strip()
        
        documents.append(project_text)
        
        # Create metadata for filtering and context
        metadata = {
            'project_id': project.get('id', ''),
            'en_name': project.get('en_name', ''),
            'ar_name': project.get('ar_name', ''),
            'developer': project.get('developer_name', ''),
            'city': project.get('city', ''),
            'district': project.get('district', ''),
            'property_types': project.get('properties_types', []),
            'start_price': project.get('start_price', 0),
            'area': project.get('area', 0),
            'gated': project.get('gated', False)
        }
        metadatas.append(metadata)
        ids.append(f"project_{i}")
    
    # Create embeddings for all project documents
    embeddings = embed(documents)
    
    # Create a temporary collection for real estate projects
    temp_collection = client.create_collection(name="temp_real_estate_projects")
    
    # Add projects to temporary collection
    temp_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )
    
    # Convert user query to embedding
    query_embedding = embed([query])[0]
    
    # Search for similar projects
    results = temp_collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    # Clean up temporary collection
    client.delete_collection(name="temp_real_estate_projects")
    
    # Format results for better readability
    formatted_results = []
    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        formatted_result = f"""
Project {i+1}:
Name: {metadata.get('en_name', '')} ({metadata.get('ar_name', '')})
Developer: {metadata.get('developer', '')}
Location: {metadata.get('city', '')} - {metadata.get('district', '')}
Property Types: {', '.join(metadata.get('property_types', []))}
Starting Price: {metadata.get('start_price', 0):,} EGP
Area: {metadata.get('area', 0)} sqm
Gated Community: {metadata.get('gated', False)}

Full Details:
{doc}
        """.strip()
        formatted_results.append(formatted_result)
    
    return formatted_results