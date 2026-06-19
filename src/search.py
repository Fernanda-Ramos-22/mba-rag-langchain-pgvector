import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector


def get_vectorstore():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "pdf_chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )


def search_context(question: str) -> str:
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_score(question, k=10)

    contexts = []

    for document, score in results:
        contexts.append(document.page_content)

    return "\n\n---\n\n".join(contexts)