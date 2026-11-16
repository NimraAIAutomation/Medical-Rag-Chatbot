import streamlit as st
from src.document_processor import extract_pdf
from src.chunking import create_chunks
from src.embeddings import generate_embeddings
from src.vector_store import store_chunks
from src.retrieval import retrieve_relevant_chunks
from src.chatbot import generate_answer

st.set_page_config(
    page_title="Medical RAG Chatbot",
    layout="wide"
)

st.title("Medical RAG Chatbot")

st.caption(
    "Ask questions using uploaded clinical guideline documents."
)


# Sidebar
st.sidebar.header("Configuration")

chunk_size = st.sidebar.slider(
    "Chunk Size",
    min_value=200,
    max_value=1500,
    value=500,
    step=100
)

overlap = st.sidebar.slider(
    "Chunk Overlap",
    min_value=0,
    max_value=300,
    value=100,
    step=50
)

top_k = st.sidebar.slider(
    "Retrieved Passages",
    min_value=1,
    max_value=10,
    value=3
)

threshold = st.sidebar.slider(
    "Relevance Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.05
)


# Document upload
st.header("1. Upload Clinical Guidelines")

uploaded_files = st.file_uploader(
    "Upload clinical PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("Process Documents"):

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")

    else:

        try:
            all_chunks = []

            with st.spinner("Processing documents..."):

                for uploaded_file in uploaded_files:

                    documents = extract_pdf(uploaded_file)

                    chunks = create_chunks(
                        documents,
                        chunk_size=chunk_size,
                        overlap=overlap
                    )

                    all_chunks.extend(chunks)

                if not all_chunks:
                    st.error("No extractable text found.")
                else:

                    embeddings = generate_embeddings(all_chunks)

                    collection = store_chunks(
                        all_chunks,
                        embeddings
                    )

                    st.session_state["indexed"] = True

                    st.success("Documents indexed successfully!")

                    st.write("Documents:", len(uploaded_files))
                    st.write("Extracted chunks:", len(all_chunks))
                    st.write("Total database records:", collection.count())

        except Exception as e:
            st.error(f"Document processing failed: {e}")


st.divider()


# Question and answer
st.header("2. Ask a Medical Question")

question = st.text_area(
    "Enter your question",
    placeholder="Example: What is diabetes and how is it treated?"
)


if st.button("Generate Answer", type="primary"):

    if not question or not question.strip():

        st.warning("Please enter a valid question.")

    elif not st.session_state.get("indexed", False):

        st.warning("Please process clinical documents first.")

    else:

        try:

            with st.spinner("Searching clinical guidelines..."):

                from src.vector_store import store_chunks
                import chromadb

                client = chromadb.PersistentClient(
                    path="chroma_db"
                )

                collection = client.get_collection(
                    name="medical_guidelines"
                )

                retrieved = retrieve_relevant_chunks(
                    question,
                    collection,
                    top_k=top_k,
                    threshold=threshold
                )

            if not retrieved:

                st.warning(
                    "No sufficiently relevant information "
                    "was found in the uploaded guidelines."
                )

            else:

                with st.spinner("Generating answer..."):

                    answer = generate_answer(
                        question,
                        retrieved
                    )

                st.subheader("Answer")
                st.write(answer)

                st.subheader("Retrieved Sources")

                for i, result in enumerate(retrieved, start=1):

                    metadata = result["metadata"]

                    with st.expander(f"Source {i}"):

                        st.write(
                            "**Document:**",
                            metadata.get("source", "Unknown")
                        )

                        st.write(
                            "**Page:**",
                            metadata.get("page_number", "Unknown")
                        )

                        st.write(
                            "**Section:**",
                            metadata.get("section", "Not identified")
                        )

                        st.write(
                            "**Similarity:**",
                            round(result["similarity"], 4)
                        )

                        st.write("**Passage:**")
                        st.write(result["text"])

        except Exception as e:

            st.error(f"Chatbot error: {e}")


st.divider()

st.caption(
    "For educational and research purposes only. "
    "This chatbot does not replace professional medical advice."
)
