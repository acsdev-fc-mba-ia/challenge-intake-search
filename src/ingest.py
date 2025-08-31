import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector

load_dotenv()

def get_pdf_path() -> Path:
    """Get the absolute path to the PDF file."""
    current_dir = Path(__file__).parent
    pdf_path = current_dir / os.getenv("PDF_PATH")
    print(f"PDF Path: {pdf_path}")
    return pdf_path

PDF_PATH = get_pdf_path()
LLM_API_KEY = os.getenv("LLM_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")


def validate_environment():
    """Validate environment variables."""
    if not PDF_PATH or not PDF_PATH.exists():
        raise ValueError("Invalid PDF PATH: PDF_PATH environment variable or file do not exist")

    for k in (LLM_API_KEY, DATABASE_URL, PG_VECTOR_COLLECTION_NAME):
        if not k:
            raise RuntimeError(f"Environment variable {k} is not set")

def get_chunks() -> list[Document]:
    """Load PDF and split into chunks."""
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    return clean_chunks(chunks)

def clean_chunks(chunks: list[Document]) -> list[Document]:
    """Remove empty metadata fields from document chunks."""
    return [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]

def cleanDB(embeddings: Embeddings):
    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )
    try:
        pgvector.drop_tables()
    except Exception as e:
        print(f"Error dropping tables: {e}")

def persist_embeddings(chunks: list[Document]):
    """Persist document embeddings to the database."""
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=LLM_API_KEY, model="models/embedding-001")

    cleanDB(embeddings) # Avoid data duplication

    chunk_ids = [f"doc-{i}" for i in range(len(chunks))]

    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )
    pgvector.create_tables_if_not_exists()
    pgvector.add_documents(documents=chunks, ids=chunk_ids)

def search_pdf(query: str) -> list[Document]:
    """Search for documents in the PDF database.

    Args:
        query (str): The search query.

    Returns:
        list[Document]: A list of relevant documents.
    """
    embeddings = GoogleGenerativeAIEmbeddings(google_api_key=LLM_API_KEY, model="models/embedding-001")
    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )
    return pgvector.similarity_search(query, k=10)

def ingest_pdf():
    chunks = get_chunks()
    persist_embeddings(chunks)

if __name__ == "__main__":
    validate_environment()
    ingest_pdf()
    print("Ingestion complete.")