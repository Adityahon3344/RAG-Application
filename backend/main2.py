from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from database import addData, getData
from service import findResponse

app = FastAPI(title="RAG Agent Application")


class DocumentInput(BaseModel):
    documents: list[str]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatInput(BaseModel):
    prompt: str
    history: list[ChatMessage] = Field(default_factory=list)


@app.get("/")
def home():
    return "Welcome to RAG Agent Application!"


@app.post("/collection")
def storeData(data: DocumentInput):
    addData(data.documents)
    return {"message": "Documents stored successfully!"}


@app.get("/collection")
def getCollectionData():
    return getData()


@app.post("/chat")
def getResponse(query: ChatInput):
    history = [
        {"role": message.role, "content": message.content}
        for message in query.history
    ]
    result = findResponse(query.prompt, history)

    return {
        "response": result["answer"],
        "tools_used": result["tools_used"]
    }