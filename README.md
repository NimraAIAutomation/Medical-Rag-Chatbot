# Medical RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers medical questions using information retrieved from uploaded clinical guideline documents.

The application combines document processing, text embeddings, vector similarity search, and Large Language Models (LLMs) to generate context-based answers with source information.

## Project Overview

The goal of this project is to build a medical document-based question-answering system that reduces unsupported answers by grounding LLM responses in relevant clinical guideline passages.

Users can upload PDF documents, configure text chunking and retrieval settings, and ask questions through an interactive Streamlit interface.

## Features

- Upload clinical guideline PDF documents.
- Extract text and page-level metadata using PyMuPDF.
- Split documents into smaller overlapping chunks.
- Generate text embeddings using Sentence Transformers.
- Store embeddings and document metadata in ChromaDB.
- Retrieve relevant passages using cosine similarity.
- Configure chunk size, overlap, top-k retrieval, and similarity threshold.
- Generate context-based answers using the Groq API.
- Display retrieved passages and their source information.
- Provide fallback responses when relevant information is not retrieved.
- Interactive Streamlit interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Embedding model |
| ChromaDB | Vector database |
| Groq API | LLM integration |
| openai/gpt-oss-20b | Answer generation model |
| python-dotenv | Environment variable management |

## RAG Architecture

```text
       Clinical PDF Documents
                 |
                 v
          PDF Text Extraction
                 |
                 v
            Text Chunking
                 |
                 v
          Embedding Generation
                 |
                 v
            ChromaDB Storage
                 |
                 |
User Question   |
      |         |
      v         |
Query Embedding |
      |         |
      v         v
       Similarity Search
                 |
                 v
        Relevant Passages
                 |
                 v
          Groq LLM API
                 |
                 v
         Generated Answer
                 |
                 v
        Answer + Source Info
```

## Project Structure

```text
medical_rag_chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── src/
│   ├── document_processor.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   ├── chatbot.py
│   └── evaluation.py
│
├── data/
│
└── chroma_db/
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/medical_rag_chatbot.git
cd medical_rag_chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get an API key from the [Groq Console](https://console.groq.com/).

**Important:** Never upload your `.env` file or API key to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Start the Streamlit application.
2. Upload one or more clinical guideline PDF documents.
3. Configure chunk size and overlap.
4. Select the number of retrieved passages (top-k).
5. Set the similarity threshold.
6. Click **Process Documents** to extract, chunk, embed, and index the documents.
7. Enter a medical question.
8. Click **Generate Answer**.
9. Review the generated response and retrieved source passages.

## Example Questions

Using the sample diabetes guideline:

- What is type 2 diabetes?
- Why can blood glucose become higher than normal in type 2 diabetes?
- What are the common symptoms of diabetes?
- What risk factors are associated with diabetes?
- What general management approaches are described?

Questions outside the uploaded documents should trigger the fallback response when no relevant passages meet the retrieval threshold.

## Evaluation

The initial development test used a sample diabetes guideline PDF.

| Metric | Initial result |
|---|---|
| Documents uploaded | 1 |
| Extracted chunks | 7 |
| Embedding dimensions | 384 |
| Embedding model | all-MiniLM-L6-v2 |
| Initial similarity threshold | 0.50 |
| Maximum retrieved passages | 3 |

A separate evaluation set was prepared with answerable questions, out-of-scope questions, and an empty-query test.

Formal retrieval accuracy, answer quality, and response-time measurements still need to be completed.

## Current Limitations

- The similarity threshold is experimental and requires evaluation.
- Character-based chunking may split meaningful sections or sentences.
- Section-level metadata and citation accuracy need further improvement.
- Persistent database records must be managed carefully when documents are re-indexed.
- LLM-generated answers require verification against retrieved passages.
- The current sample dataset is for development and testing, not clinical validation.

## Future Improvements

- Improve section-aware and semantic chunking.
- Make source citations fully metadata-driven.
- Prevent stale records when re-indexing documents.
- Add retrieval precision, recall, and hit-rate evaluation.
- Measure retrieval and generation response times.
- Test with multiple trusted clinical guideline documents.
- Add support for scanned PDFs and OCR.
- Improve answer faithfulness and relevance evaluation.

## Medical Disclaimer

This project is an educational and technical prototype.

It is not a medical diagnostic system and must not replace professional medical advice, diagnosis, or treatment. Generated responses should always be checked against authoritative clinical guidelines and qualified healthcare professionals.

## Author

Developed as a hands-on project to learn and implement:

- Retrieval-Augmented Generation (RAG)
- Clinical document processing
- Text embeddings and vector databases
- Semantic similarity search
- LLM integration
- Streamlit application development

---

**Project:** Medical RAG Chatbot  
**Status:** Core implementation completed; evaluation and citation improvements ongoing.
