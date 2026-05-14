from fastapi import FastAPI
from pydantic import BaseModel

from app.ingest import ingest_documents
from app.vector_store import PineconeStore
from app.rag import RAGPipeline
from app.agent import Agent

app = FastAPI()

vectorstore = PineconeStore()

rag = RAGPipeline(vectorstore)

agent = Agent()


class AskRequest(BaseModel):

    question: str


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/ingest")
def ingest():

    count = ingest_documents()

    return {
        "message": "Documents ingested successfully",
        "chunks": count
    }


@app.post("/ask")
def ask(payload: AskRequest):

    return agent.route(
        payload.question,
        rag
    )