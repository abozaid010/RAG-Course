import json
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.retriever import retriever
from app.config import settings

class DataIngestor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def ingest_documents(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        documents = self._prepare_documents(data)
        chunks = self.splitter.split_documents(documents)
        retriever.vector_store.add_documents(chunks)

    def _prepare_documents(self, data: dict):
        docs = []
        for project in data.get("projects", []):
            content = self._format_project(project)
            docs.append(Document(page_content=content, metadata={"id": project["id"]}))
        return docs

    def _format_project(self, project: dict):
        return (
            f"Project: {project['en_name']} ({project['ar_name']})\n"
            f"Developer: {project['developer_name']}\n"
            f"Location: {project['district']}, {project['city']}\n"
            f"Price starts at: {project['start_price']}\n"
            f"Types: {', '.join(project['properties_types'])}\n"
            f"Description: {project['description']}"
        )

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_path, "test_data.json")
    ingestor = DataIngestor()
    ingestor.ingest_documents(json_path)
