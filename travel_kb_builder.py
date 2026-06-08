import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def ingest_pdf():

    pdf_path = "C:/Analytics/Airline_Chatbot/Data/SPAIN-VISA-REQUIREMENTS.pdf"
    db_path = "C:/Analytics/Airline_Chatbot/travel_vectorstore"
    collection_name = "travel_requirements"

    if not os.path.exists(pdf_path):
        print("PDF file not found")
        return

    # Connect to Chroma
    client = chromadb.PersistentClient(path=db_path)

    print("Loading PDF...")

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    # Chunk the document --- split text intelligently, typically respecting sentences or paragraphs as much as possible.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=70
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Load embedding model--- is a class (likely from a library like LangChain).
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"        #A lightweight, fast model designed for sentence-level embeddings.
    )

    print("Generating embeddings and storing in ChromaDB...")

    # Store in ChromaDB
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_path,
        collection_name=collection_name
    )

    print("Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_pdf()