from app.embeddings import EmbeddingModel
#from app.llm import LLM
from app.llm import OllamaLLM

class RAGPipeline:

    def __init__(self, vectorstore):

        self.embedder = EmbeddingModel()

        self.vs = vectorstore

        #self.llm = LLM()
        self.llm = OllamaLLM()

    def ask(self, question):

        query_embedding = self.embedder.embed(
            [question]
        )[0]

        results = self.vs.search(
            query_embedding=query_embedding,
            top_k=3
        )

        filtered = []

        for r in results:

            if r["score"] >= 0.55:

                filtered.append(r)

        if len(filtered) == 0:

            return {
                "answer": (
                    "Sorry, I don't know based "
                    "on the provided documents."
                ),

                "sources": [],

                "confidence": "low"
            }

        context = "\n\n".join([
            r["chunk"]
            for r in filtered
        ])

        prompt = f"""
You are a professional healthcare AI assistant.

IMPORTANT:
- Answer ONLY from context
- Do NOT hallucinate
- Keep answer concise

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        answer = self.llm.generate(prompt)

        top_score = filtered[0]["score"]

        confidence = (
            "high"
            if top_score >= 0.80
            else "medium"
        )

        sources = [
            {
                "document": r["document"],
                "chunk": r["chunk"]
            }
            for r in filtered
        ]

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }