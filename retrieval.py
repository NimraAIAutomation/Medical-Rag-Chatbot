
from src.embeddings import model


def retrieve_relevant_chunks(
    question,
    collection,
    top_k=3,
    threshold=0.50
):

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please enter a valid question.")

    if collection is None or collection.count() == 0:
        return []

    # Generate embedding directly from the question
    query_embedding = model.encode(
        question,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Search vector database
    response = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    results = []

    for text, metadata, distance in zip(
        response["documents"][0],
        response["metadatas"][0],
        response["distances"][0]
    ):

        similarity = 1 - distance

        if similarity >= threshold:

            results.append({
                "text": text,
                "metadata": metadata,
                "similarity": similarity
            })

    return results
