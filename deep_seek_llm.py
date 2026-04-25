# =============================================================================
# DEEPSEEK LLM INTEGRATION MODULE
# =============================================================================
# 
# PURPOSE: This module handles communication with DeepSeek's Large Language Model API.
# It's the generation component of our RAG system that creates responses based on
# retrieved context and user queries.
#
# KEY CONCEPTS:
# 1. LLM API Integration: Making HTTP requests to external AI services
# 2. Async Programming: Non-blocking requests for better performance
# 3. Chat Completions: Structured conversation format for LLM interactions
# 4. Temperature Control: Balancing creativity vs. reliability in responses
#
# WHY WE NEED THIS:
# - Provides the "Generation" part of RAG (Retrieval-Augmented Generation)
# - Converts retrieved context into natural language answers
# - Handles complex reasoning and synthesis of information
# - Scales to handle multiple concurrent requests efficiently
# =============================================================================

import httpx  # Async HTTP client for making API calls to DeepSeek
import os      # Environment variable access for API key security

# Retrieve API key from environment variables
# WHY ENVIRONMENT VARIABLES:
# - Security: API keys are sensitive credentials that shouldn't be hardcoded
# - Flexibility: Different environments (dev/staging/prod) can use different keys
# - Best Practice: Follows 12-factor app methodology for configuration
# 
# HOW TO SET: export DEEPSEEK_API_KEY="your_api_key_here" or use .env file
API_KEY = "sk-b0070ace2ad040f7b22b2e1a6dff2beb" #os.getenv("DEEPSEEK_API_KEY")


async def ask_llm(prompt: str):
    """
    Send a prompt to DeepSeek's LLM and get the response.
    
    This function is the core of the generation component in our RAG system.
    It takes the context-enhanced prompt and returns an intelligent response.
    
    PARAMETERS:
        prompt (str): The complete prompt including context and user question
    
    RETURNS:
        str: The LLM's response to the prompt
    
    HOW IT FITS IN RAG:
    1. Retrieval: Vector store finds relevant documents
    2. Augmentation: Prompt builder combines context with question
    3. Generation: This function sends the augmented prompt to LLM
    4. Response: LLM generates answer based on provided context
    
    WHY ASYNC:
    - Non-blocking: Doesn't freeze the application while waiting for response
    - Scalability: Can handle multiple concurrent requests efficiently
    - Performance: Better resource utilization in web applications
    """
    # DeepSeek API endpoint for chat completions
    # This follows OpenAI-compatible API format
    url = "https://api.deepseek.com/v1/chat/completions"

    # HTTP headers for authentication and content type
    # Bearer token authentication is standard for API security
    print(f"API_KEY: {API_KEY}")
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # API authentication
        "Content-Type": "application/json"      # Specify JSON payload
    }

    # Request payload with model configuration
    # This structure follows OpenAI API standards for compatibility
    data = {
        "model": "deepseek-chat",  # DeepSeek's chat model (similar to GPT-3.5/4)
        "messages": [
            {
                "role": "user",      # Message role (user/assistant/system)
                "content": prompt     # The actual prompt content
            }
        ],
        "temperature": 0.1  # Controls randomness: 0=deterministic, 1=creative
    }

    # Make async HTTP request to DeepSeek API
    # AsyncClient provides non-blocking HTTP requests
    # Context manager ensures proper connection cleanup
    async with httpx.AsyncClient() as client:
        # Send POST request with headers and JSON payload
        res = await client.post(url, headers=headers, json=data)
        response_content = res.json()["choices"][0]["message"]["content"]
        print(f"respsoen \n\n\ {response_content}")
        # Parse JSON response and extract the answer
        # Response structure: {"choices": [{"message": {"content": "answer"}}]}
        return response_content




if __name__ == "__main__":
    import asyncio
    async def main():

        data = """


                {
  "brand": "Toshiba",
  "category": "Dishwashers",
  "models": [
    {
      "model_number": "DW-GZ202",
      "series": "Gaza202",
      "capacity": "12 place settings",
      "energy_efficiency": "A+++",
      "release_year": 2021,
      "insurance_years": {
        "standard_warranty": 2,
        "extended_warranty_available": true,
        "max_insurance_years": 5
      },
      "features": ["Smart Wash", "Half Load", "Delay Start", "AquaStop"]
    },
    {
      "model_number": "DW-3680",
      "series": "Premium",
      "capacity": "15 place settings",
      "energy_efficiency": "A++",
      "release_year": 2022,
      "insurance_years": {
        "standard_warranty": 3,
        "extended_warranty_available": true,
        "max_insurance_years": 7
      },
      "features": ["WiFi Connect", "Auto Door Open", "Power Dry", "Child Lock"]
    },
    {
      "model_number": "DW-1890",
      "series": "Compact",
      "capacity": "9 place settings",
      "energy_efficiency": "A++",
      "release_year": 2020,
      "insurance_years": {
        "standard_warranty": 2,
        "extended_warranty_available": false,
        "max_insurance_years": 2
      },
      "features": ["Space Saving", "Quick Wash", "LED Display"]
    },
    {
      "model_number": "DW-4200X",
      "series": "Professional",
      "capacity": "16 place settings",
      "energy_efficiency": "A+++",
      "release_year": 2023,
      "insurance_years": {
        "standard_warranty": 3,
        "extended_warranty_available": true,
        "max_insurance_years": 8
      },
      "features": ["Triple Zone", "Steam Clean", "Smart Diagnosis", "Quiet Operation"]
    },
    {
      "model_number": "DW-2750",
      "series": "Standard",
      "capacity": "13 place settings",
      "energy_efficiency": "A+",
      "release_year": 2019,
      "insurance_years": {
        "standard_warranty": 2,
        "extended_warranty_available": true,
        "max_insurance_years": 4
      },
      "features": ["Multi Wash Programs", "Salt Indicator", "Rinse Aid Alert"]
    },
    {
      "model_number": "DW-5120",
      "series": "Smart Home",
      "capacity": "14 place settings",
      "energy_efficiency": "A+++",
      "release_year": 2024,
      "insurance_years": {
        "standard_warranty": 4,
        "extended_warranty_available": true,
        "max_insurance_years": 10
      },
      "features": ["Voice Control", "App Control", "AI Wash Detection", "Self Cleaning"]
    },
    {
      "model_number": "DW-3320",
      "series": "Eco",
      "capacity": "12 place settings",
      "energy_efficiency": "A++++",
      "release_year": 2023,
      "insurance_years": {
        "standard_warranty": 3,
        "extended_warranty_available": true,
        "max_insurance_years": 6
      },
      "features": ["Low Water Consumption", "Eco Mode", "Quick Eco Wash"]
    },
    {
      "model_number": "DW-4600",
      "series": "Family",
      "capacity": "15 place settings",
      "energy_efficiency": "A++",
      "release_year": 2022,
      "insurance_years": {
        "standard_warranty": 2,
        "extended_warranty_available": true,
        "max_insurance_years": 5
      },
      "features": ["Large Capacity", "Flexible Racking", "Intensive Wash", "Gentle Care"]
    },
    {
      "model_number": "DW-2100",
      "series": "Basic",
      "capacity": "10 place settings",
      "energy_efficiency": "A+",
      "release_year": 2021,
      "insurance_years": {
        "standard_warranty": 1,
        "extended_warranty_available": false,
        "max_insurance_years": 1
      },
      "features": ["Simple Controls", "Basic Programs", "Compact Design"]
    },
    {
      "model_number": "DW-5850",
      "series": "Ultra Premium",
      "capacity": "18 place settings",
      "energy_efficiency": "A+++",
      "release_year": 2024,
      "insurance_years": {
        "standard_warranty": 5,
        "extended_warranty_available": true,
        "max_insurance_years": 12
      },
      "features": ["Ultra Quiet", "Advanced Sensors", "Custom Wash Cycles", "Premium Materials"]
    }
  ],
  "insurance_info": {
    "standard_coverage": ["Parts and Labor", "Manufacturing Defects"],
    "extended_coverage": ["Annual Maintenance", "Accidental Damage", "Power Surge Protection"],
    "service_network": "Global Toshiba Service Centers",
    "claim_process": "24/7 Online Portal + Phone Support"
  },
  "last_updated": "2024-04-25"
}





"""


# 20 page tite: 
        result = await ask_llm("""
        You are toshiba engineer, answer the following question based on the provided context.
        
        Question: How can I start: DW-GZ202?

        Data source: 
       

        """)
        print(result)
    
    asyncio.run(main())