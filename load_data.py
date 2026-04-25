# =============================================================================
# DATA INGESTION MODULE - Loading Real Estate Data into RAG System
# =============================================================================
# 
# PURPOSE: This script handles the initial data loading process for our RAG system.
# It reads real estate project data from a JSON file and loads it into the
# vector database (ChromaDB) for later retrieval.
#
# KEY CONCEPTS:
# 1. Data Ingestion: Process of loading data into the system
# 2. JSON Parsing: Reading structured data from JSON files
# 3. Vector Population: Adding documents to the vector database
# 4. Batch Processing: Efficiently handling multiple documents at once
#
# WHY THIS IS IMPORTANT:
# - Initializes the knowledge base for our RAG system
# - Converts raw data into searchable vector embeddings
# - Enables semantic search capabilities
# - Provides the foundation for accurate RAG responses
#
# USAGE:
# Run this script once to populate the vector database with real estate data
# python load_data.py
# =============================================================================

import json  # JSON parsing library for reading structured data
from vector_store import add_projects  # Our vector database insertion function

# Open and read the JSON file containing real estate project data
# The 'with' statement ensures proper file handling and automatic closure
# projects.json should contain structured real estate project information
with open("test_data.json") as f:
    data = json.load(f)

# Extract the projects list from the JSON structure
# The JSON structure has: {"projects": [...]}
projects = data["projects"]

# WHY THIS DATA STRUCTURE:
# - "data" wrapper allows for metadata (pagination, totals, etc.)
# - "projects" array contains individual project records
# - Each project should have fields like name, city, price, description
# - Consistent structure enables reliable parsing and processing

# Load the projects into the vector database
# This function will:
# 1. Process each project into a text document
# 2. Generate embeddings for semantic search
# 3. Store documents, metadata, and embeddings in ChromaDB
# 4. Create indexes for fast retrieval
add_projects(projects)

# WHY BATCH PROCESSING:
# - More efficient than processing one document at a time
# - Reduces API calls and database connections
# - Ensures consistent embedding generation
# - Better memory utilization and performance

# Confirmation message
# Provides feedback that the data loading process completed successfully
# This is important for debugging and verification purposes
print("Data inserted into Chroma")

# =============================================================================
# DATA INGESTION BEST PRACTICES:
# =============================================================================
# 
# 1. DATA VALIDATION:
#    - Always validate JSON structure before processing
#    - Check for required fields in each project
#    - Handle missing or malformed data gracefully
# 
# 2. ERROR HANDLING:
#    - Wrap file operations in try-catch blocks
#    - Handle network issues if loading from URLs
#    - Log errors for debugging and monitoring
# 
# 3. PERFORMANCE:
#    - Process data in batches for large datasets
#    - Monitor memory usage during embedding generation
#    - Consider progress indicators for long operations
# 
# 4. DATA QUALITY:
#    - Clean and normalize text before embedding
#    - Remove duplicate or irrelevant information
#    - Ensure consistent formatting across documents
# 
# 5. MONITORING:
#    - Track number of documents processed
#    - Monitor embedding generation time
#    - Log any skipped or failed documents
# =============================================================================

# =============================================================================
# NEXT STEPS AFTER DATA LOADING:
# =============================================================================
# 
# After running this script:
# 1. Verify data was loaded correctly by checking ChromaDB
# 2. Test the vector search with sample queries
# 3. Start the FastAPI server: uvicorn main:app --reload
# 4. Test the complete RAG workflow via API calls
# 5. Monitor performance and accuracy of responses
# =============================================================================