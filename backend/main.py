from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from database import addData
from services import findResponse


app = FastAPI(title="RAG Application")


class DocumentInput(BaseModel):
    document: Optional[list[str]] = None
    documents: Optional[list[str]] = None

    @property
    def entries(self) -> list[str]:
        return self.document if self.document is not None else (self.documents or [])


class ChatInput(BaseModel):
    prompt: str


@app.get('/')
def root():
    return {"status": "ok", "message": "RAG backend running"}


@app.get('/home')
def home():
    return "welcome to RAG"


@app.post('/collection')
def storeData(document: DocumentInput):
    entries = document.entries
    if not entries:
        return {"status": "error", "message": "No documents provided."}

    addData(entries)
    return {"status": "success", "stored": len(entries)}


@app.post('/chat')
def chat(prompt: ChatInput):
    if not prompt.prompt or not prompt.prompt.strip():
        return {"response": "Please provide a valid question."}

    return {"response": findResponse(prompt.prompt)}