from google import genai
from dotenv import load_dotenv
import os

from database import askQuestion
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def create_prompt(question: str) -> str:

    chunks = askQuestion(question)

    context = ""

    for doc in chunks:
        context += doc.page_content + "\n\n"
        
    prompt_template = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant.

        Use relevant information from the context when it helps answer
        questions about the user's documents. If the context is empty or
        does not answer the question, respond using your general knowledge.
        Do not present general knowledge as if it came from the documents.

        Context:
        {context}

        Question:
        {question}

        Answer:
    """)

    formatted_prompt = prompt_template.invoke({
        "context": context,
        "question": question
    })

    return formatted_prompt.to_string()


def findResponse(question: str) -> str:

    final_prompt = create_prompt(question)

    response = client.models.generate_content(
        model="models/gemini-3.1-flash-lite",
        contents=final_prompt
    )

    return response.text