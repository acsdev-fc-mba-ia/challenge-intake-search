import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
LLM_API_KEY = os.getenv("LLM_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")

def validate_environment():
    """Validate environment variables."""
    if not PDF_PATH or not Path(PDF_PATH).exists():
        raise ValueError("Invalid PDF_PATH environment variable")

    for k in (LLM_API_KEY, DATABASE_URL, PG_VECTOR_COLLECTION_NAME):
        if not k:
            raise RuntimeError(f"Environment variable {k} is not set")

def get_chunks() -> list[Document]:
    """Load PDF and split into chunks."""
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    return chunks

def clean_chunks(chunks: list[Document]) -> list[Document]:
    """Remove empty metadata fields from document chunks."""
    return [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]    

def persist_embeddings(chunks: list[Document]):
    """Persist document embeddings to the database."""
    chunk_ids = [f"doc-{i}" for i in range(len(chunks))]

    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=LLM_API_KEY, model="models/embedding-001")

    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )
    # pgvector.delete_collection() # clear existing embeddings in there is any
    pgvector.add_documents(documents=chunks, ids=chunk_ids)

def ingest_pdf():
    chunks = get_chunks()
    chunks = clean_chunks(chunks)
    persist_embeddings(chunks)

if __name__ == "__main__":
    validate_environment()
    ingest_pdf()