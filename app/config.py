import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_store")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_data")
    TOP_K = int(os.getenv("TOP_K", 5))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

settings = Settings()
