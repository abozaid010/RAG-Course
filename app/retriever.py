from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from app.config import settings

class KnowledgeRetriever:
    def __init__(self):
        self.embeddings = FastEmbedEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.vector_store = Chroma(
            persist_directory=settings.VECTOR_DB_PATH,
            embedding_function=self.embeddings,
            collection_name=settings.COLLECTION_NAME
        )

    def search(self, query: str):
        results = self.vector_store.similarity_search(
            query, 
            k=settings.TOP_K
        )
        return "\n\n".join([doc.page_content for doc in results])

retriever = KnowledgeRetriever()
