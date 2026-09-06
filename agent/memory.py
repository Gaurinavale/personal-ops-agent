import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

load_dotenv()  # ensure .env is loaded before we read GEMINI_API_KEY below

PERSIST_DIR = "chroma_memory"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)
vector_store = Chroma(
    collection_name="personal_ops_memory",
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)


def save_memory(text: str):
    doc = Document(page_content=text)
    vector_store.add_documents([doc])


def recall_memory(query: str, k: int = 3) -> list[str]:
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]