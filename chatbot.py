
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, retrieved_chunks):

    if not question or not question.strip():
        return "Please enter a valid medical question."

    if not retrieved_chunks:
        return (
            "I could not find relevant information "
            "in the uploaded clinical guidelines. "
            "Please consult a qualified healthcare professional."
        )

    # Prepare context with source information
    context = ""

    for i, chunk in enumerate(retrieved_chunks, start=1):

        metadata = chunk["metadata"]

        context += f"""
        Passage {i}
        Source: {metadata.get('source', 'Unknown')}
        Page: {metadata.get('page_number', 'Unknown')}
        Section: {metadata.get('section', 'Not identified')}

        Content:
        {chunk['text']}

        """

    prompt = f"""
    You are a medical guideline assistant.

    Answer the user's question using ONLY the
    provided clinical guideline context.

    Rules:
    - Do not use outside medical knowledge.
    - Do not invent facts or recommendations.
    - If information is insufficient, clearly say so.
    - Include source citations with page numbers.
    - Include section references when available.
    - Do not present yourself as a doctor.
    - Do not provide a diagnosis or personalized treatment.

    Clinical guideline context:
    {context}

    User question:
    {question}

    Provide a clear, concise answer with citations.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content
