import os

# HIDE WARNINGS + LOGS + PROGRESS BARS

os.environ["TOKENIZERS_PARALLELISM"] = "false"

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

os.environ["HF_HUB_VERBOSITY"] = "error"


from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(self, texts):

        embeddings = self.model.encode(
            texts,
            show_progress_bar=False
        )

        return embeddings.tolist()