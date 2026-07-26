from backend.config.settings import logger

try:
    import chromadb
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    logger.warning("chromadb not installed. Vector Search Tool will run in mock mode.")


class VectorSearchTool:

    def __init__(self):
        if HAS_CHROMA:
            self.client = chromadb.PersistentClient(
                path="backend/chroma_db"
            )

            self.collection = self.client.get_or_create_collection(
                name="patents"
            )

    def store_patents(self, patents: list, embeddings: list):

        if not HAS_CHROMA:
            logger.info(f"Mock stored {len(patents)} patents.")
            return

        BATCH_SIZE = 100

        for start in range(0, len(patents), BATCH_SIZE):

            end = start + BATCH_SIZE

            batch_patents = patents[start:end]
            batch_embeddings = embeddings[start:end]

            ids = [p.patent_number for p in batch_patents]

            docs = [p.abstract for p in batch_patents]

            metadatas = [
                {
                    "title": p.title,
                    "provider": p.provider
                }
                for p in batch_patents
            ]

            try:

                self.collection.add(
                    ids=ids,
                    embeddings=batch_embeddings,
                    documents=docs,
                    metadatas=metadatas
                )

                logger.info(
                    f"Stored batch {start + 1}-{min(end, len(patents))}"
                )

            except Exception as e:

                logger.error(
                    f"Failed batch {start + 1}: {e}"
                )

        logger.info("Finished storing all patents.")

    def search_similar(
        self,
        query_embedding: list,
        n_results: int = 5
    ):

        if not HAS_CHROMA:
            logger.info("Mock vector search.")
            return None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        logger.info(
            f"Retrieved {len(results['ids'][0])} similar patents."
        )

        return results