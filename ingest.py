"""
ingest.py
---------
Step 1 of the RAG pipeline: DOCUMENT INGESTION + CHUNKING + EMBEDDING.

What this script does:
1. Loads every .txt file from the data/ folder
2. Splits each document into overlapping chunks (so the LLM gets focused context, not entire files)
3. Converts each chunk into a vector using OpenAI's embedding model
4. Saves all those vectors into a local FAISS index on disk

Run this ONCE (or whenever you add new notes to data/):
    python ingest.py
"""
"""
ingest.py
---------
Step 1 of the RAG pipeline: DOCUMENT INGESTION + CHUNKING + EMBEDDING.

What this script does:
1. Loads every .txt file from the data/ folder
2. Splits each document into overlapping chunks (so the LLM gets focused context, not entire files)
3. Converts each chunk into a vector using OpenAI's embedding model
4. Saves all those vectors into a local FAISS index on disk

Run this ONCE (or whenever you add new notes to data/):
    python ingest.py
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load GOOGLE_API_KEY from a local .env file (never hardcode your key in code)
load_dotenv()

DATA_DIR = "data"
INDEX_DIR = "faiss_index"


def load_documents():
    """Load every .txt file inside data/ as a LangChain Document object."""
    loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s) from '{DATA_DIR}/'")
    return documents


def chunk_documents(documents):
    """
    Split documents into overlapping chunks.

    chunk_size=800     -> roughly a few paragraphs per chunk
    chunk_overlap=150  -> keeps context continuous across chunk boundaries
                           (e.g. so a definition split across two chunks isn't lost)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s)")
    return chunks


def build_and_save_index(chunks):
    """Embed all chunks and persist them to a local FAISS index."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(INDEX_DIR)
    print(f"FAISS index saved to '{INDEX_DIR}/'")


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    build_and_save_index(chunks)
    print("\nIngestion complete. You can now run chatbot.py to ask questions.")