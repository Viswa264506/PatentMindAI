from typing import List

from backend.tools.embedding_tool import EmbeddingTool
from backend.tools.vector_search_tool import VectorSearchTool
from backend.schemas.state import ResearchPlan, Patent
from backend.config.settings import logger
from backend.agents.patent_reranker_agent import PatentRerankerAgent

class PatentSearchService:

    TOP_K = 25

    def __init__(self):
        self.embedding_tool = EmbeddingTool()
        self.vector_tool = VectorSearchTool()
        self.reranker = PatentRerankerAgent()

    def execute_search_strategy(
        self,
        user_invention: str,
        research_plan: ResearchPlan
    ) -> List[Patent]:

        logger.info("Starting semantic patent search...")

        retrieved_patents = {}
        query_count = 0

        for query in research_plan.search_queries:

            logger.info(f"Searching for: {query}")

            query_embedding = self.embedding_tool.get_embedding(query)

            results = self.vector_tool.search_similar(
    query_embedding=query_embedding,
    n_results=30
)

            if not results:
                continue

            ids = results.get("ids", [[]])[0]
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]

            # Build keyword list from research plan
            keywords = set()

            for word in research_plan.technical_keywords:
                keywords.add(word.lower())

            for word in research_plan.important_concepts:
                keywords.add(word.lower())

            for patent_id, document, metadata in zip(
                ids,
                documents,
                metadatas
            ):

                title = metadata.get("title", "").lower()
                abstract = document.lower()

                # Count keyword matches
                score = 0
                for keyword in keywords:
                    if keyword in title or keyword in abstract:
                        score += 1

                # Skip weak matches
                if score < 1:
                    continue

                if patent_id not in retrieved_patents:

                    retrieved_patents[patent_id] = Patent(
                        patent_number=patent_id,
                        title=metadata.get("title", "Unknown"),
                        abstract=document,
                        provider=metadata.get(
                            "provider",
                            "Lens Dataset"
                        )
                    )

                if patent_id not in retrieved_patents:

                    retrieved_patents[patent_id] = Patent(
                        patent_number=patent_id,
                        title=metadata.get("title", "Unknown"),
                        abstract=document,
                        provider=metadata.get(
                            "provider",
                            "Lens Dataset"
                        )
                    )

            query_count += 1

        logger.info(
            f"Executed {query_count} semantic searches."
        )

        candidate_patents = list(retrieved_patents.values())

        logger.info(
            f"Retrieved {len(candidate_patents)} candidate patents."
)

        reranked_patents = self.reranker.rerank(
            user_invention=user_invention,
            patents=candidate_patents
        )


        logger.info(
            f"Returning {len(reranked_patents)} reranked patents."
        )

        return reranked_patents