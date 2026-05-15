from pinecone import Pinecone, ServerlessSpec

from app.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX
)


class PineconeStore:

    def __init__(self):

        self.pc = Pinecone(
            api_key=PINECONE_API_KEY
        )

        existing_indexes = [
            index["name"]
            for index in self.pc.list_indexes()
        ]

        if PINECONE_INDEX not in existing_indexes:

            self.pc.create_index(
                name=PINECONE_INDEX,
                dimension=384,
                metric="cosine-similarity",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = self.pc.Index(
            PINECONE_INDEX
        )

    def upsert(self, vectors):

        self.index.upsert(vectors=vectors)

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        formatted = []

        for match in results["matches"]:

            formatted.append({
                "score": match["score"],
                "document": match["metadata"]["source"],
                "chunk": match["metadata"]["text"]
            })

        return formatted