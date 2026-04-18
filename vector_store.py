import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="projects"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(texts):
    return model.encode(texts).tolist()


def add_projects(projects):
    documents = []
    metadatas = []
    ids = []

    for p in projects:
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

        metadatas.append({
            "id": p.get("id"),
            "city": p.get("city"),
            "price": p.get("start_price"),
            "types": ",".join(p.get("properties_types", []))
        })

        ids.append(p.get("id"))

    embeddings = embed(documents)

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )


def query_projects(query, k=3):
    query_embedding = embed([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]