
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your backend/.env file."
    )

# Initialize Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=API_KEY
)

# Initialize ChromaDB vector store
vector_store = Chroma(
    collection_name="myCollection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


# Add documents to vector database
def addData(data: list):
    if not data:
        raise ValueError("No data provided to store.")

    try:
        vector_store.add_texts(texts=data)
        print("Data stored successfully!")
    except Exception as e:
        print(f"Error storing data: {e}")
        raise


# Retrieve all stored documents
def getData():
    try:
        data = vector_store.get()
        return data
    except Exception as e:
        print(f"Error retrieving data: {e}")
        raise


# Search for relevant documents
def askQuestion(askedQuery: str):
    if not askedQuery or not askedQuery.strip():
        raise ValueError("Please provide a valid question.")

    try:
        chunks = vector_store.similarity_search(
            query=askedQuery,
            k=2
        )
        return chunks
    except Exception as e:
        print(f"Error searching documents: {e}")
        raise
