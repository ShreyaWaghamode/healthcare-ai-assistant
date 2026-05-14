import os
import uuid
import re

from app.embeddings import EmbeddingModel
from app.vector_store import PineconeStore


def chunk_text(
    text,
    chunk_size=500,
    overlap=100
):

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) <= chunk_size:

            current_chunk += " " + sentence

        else:

            chunks.append(
                current_chunk.strip()
            )

            overlap_text = current_chunk[-overlap:]

            current_chunk = overlap_text + " " + sentence

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks


def ingest_documents():

    embedder = EmbeddingModel()

    store = PineconeStore()

    vectors = []

    DATA_FOLDER = "data"

    for file_name in os.listdir(DATA_FOLDER):

        if file_name.endswith(".txt"):

            path = os.path.join(
                DATA_FOLDER,
                file_name
            )

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read()

            chunks = chunk_text(text)

            embeddings = embedder.embed(chunks)

            for chunk, emb in zip(chunks, embeddings):

                vectors.append(
                    (
                        str(uuid.uuid4()),
                        emb,
                        {
                            "source": file_name,
                            "text": chunk
                        }
                    )
                )

    store.upsert(vectors)

    return len(vectors)