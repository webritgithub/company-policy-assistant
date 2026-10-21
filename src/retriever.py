
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from src.ingestion import load_and_split_pdf

load_dotenv()

PERSIST_DIRECTORY = "chroma_db"
COLLECTION_NAME = "employee_handbook"


def get_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    # Reuse the database if it already exists.
    if os.path.exists(PERSIST_DIRECTORY):
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings,
        )

        if vector_store._collection.count() > 0:
            return vector_store

    # Otherwise, create it from the PDF chunks.
    chunks = load_and_split_pdf()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
    )

    return vector_store


if __name__ == "__main__":
    store = get_vector_store()

    results = store.similarity_search(
        "How many annual leave days does CedarWave Analytics provide?",
        k=3,
    )

    for result in results:
        print("\nRetrieved text:")
        print(result.page_content)
        print("Metadata:", result.metadata)
