
import chromadb
import hashlib


def store_chunks(chunks, embeddings):

    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    collection_name = "medical_guidelines"

    if collection_name in [
        c.name for c in client.list_collections()
    ]:
        client.delete_collection(name=collection_name)

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
)

    ids = []

    for i, chunk in enumerate(chunks):

        unique_text = (
            f"{chunk['metadata']['source']}|"
            f"{chunk['metadata']['page_number']}|"
            f"{chunk['text']}"
        )

        chunk_id = hashlib.sha256(
            unique_text.encode("utf-8")
        ).hexdigest()

        ids.append(chunk_id)

    collection.upsert(
        ids=ids,
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        embeddings=embeddings.tolist()
    )

    return collection
