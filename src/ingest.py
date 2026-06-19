import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector


def main():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    collection_name = os.getenv("PGVECTOR_COLLECTION", "pdf_chunks")

    pdf_path = "document.pdf"

    print("📄 Carregando PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("✂️ Dividindo em chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print(f"📦 Total de chunks gerados: {len(chunks)}")

    # Limite temporário para evitar estourar a cota gratuita
    chunks = chunks[:5]

    print(f"📦 Total de chunks enviados para embedding: {len(chunks)}")

    print("🧠 Criando embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    print("🗄️ Conectando ao PGVector...")
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=database_url,
        use_jsonb=True,
    )

    print("🧹 Limpando coleção anterior...")
    vectorstore.delete_collection()
    vectorstore.create_collection()

    print("💾 Salvando documentos...")
    vectorstore.add_documents(chunks)

    print("✅ Ingestão concluída com sucesso!")


if __name__ == "__main__":
    main()