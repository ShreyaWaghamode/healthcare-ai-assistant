# Healthcare AI Assistant

AI-powered Healthcare Assistant using FastAPI, RAG, Pinecone, Sentence Transformers, and Ollama.open AI

## Features

- Retrieval-Augmented Generation (RAG)
- Semantic Search with Pinecone
- Local LLM support using Ollama
- Agentic workflow with tool routing
- Appointment slot checking tool
- FastAPI REST APIs
- Context-aware healthcare question answering

---

## Tech Stack

- FastAPI
- Pinecone
- Sentence Transformers
- Ollama
- Gemma 3B
- Python
-open Ai

---

## Project Structure

```bash
app/
│
├── main.py
├── rag.py
├── agent.py
├── ingest.py
├── embeddings.py
├── llm.py
├── vector_store.py
├── tools.py
├── config.py


data/
|
|---appointment_policy.txt
|---appointment_confirmation.txt
|---cancellation_policy.txt
|---insurance_faq.txt
|---medication_policy.txt
|---patient_rights.txt
|---telehealth_policy.txt



requirements.txt
.env
README.md

# How to run this project
1. Clone the repository
3 create virtual env 
3. Install dependencies: pip install -r requirements.txt
4. Run the app: uvicorn app.main:app --reload


Clone the repository
Create virtual env
Install dependencies: pip install -r requirements.txt
Run the app: uvicorn app.main:app --reload

then Open the http://127.0.0.1:8000/docs

and check the swagger api
health 
ingest
ask
