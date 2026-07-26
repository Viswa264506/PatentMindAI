from backend.config.settings import logger

# For development without heavy dependencies if needed, we wrap it in a try-except.
try:
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_MODEL = True
except ImportError:
    HAS_MODEL = False
    logger.warning("sentence-transformers not installed. Embedding Tool will return mock embeddings.")

class EmbeddingTool:
    def get_embedding(self, text: str) -> list[float]:
        if HAS_MODEL:
            logger.info("Generating real embedding.")
            return MODEL.encode(text).tolist()
        else:
            logger.info("Generating mock embedding.")
            return [0.1] * 384
