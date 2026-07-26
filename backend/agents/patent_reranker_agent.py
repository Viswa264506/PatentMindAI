from typing import List

from backend.agents.base import BaseAgent
from backend.schemas.state import Patent, PatentRanking
from backend.utils.prompt_formatter import to_json
from backend.config.settings import logger


class PatentRerankerAgent(BaseAgent):

    TOP_K = 8

    def __init__(self):
        super().__init__(
            prompt_filename="patent_reranker_agent.txt",
            name="Patent Reranker Agent"
        )

    def rerank(
        self,
        user_invention: str,
        patents: List[Patent]
    ) -> List[Patent]:

        logger.info("Patent Reranker Agent started.")

        if not patents:
            return []

        patents_json = to_json(patents)

        user_prompt = f"""
User Invention

{user_invention}

Candidate Patents

{patents_json}

Rank every patent from MOST relevant to LEAST relevant.

Return ONLY JSON matching PatentRanking schema.
"""

        ranking = self.execute(
            prompt=user_prompt,
            response_model=PatentRanking
        )

        patent_map = {
            p.patent_number: p
            for p in patents
        }

        ordered_patents = []

        for patent_number in ranking.patent_numbers:

            if patent_number in patent_map:
                ordered_patents.append(
                    patent_map[patent_number]
                )

        logger.info(
            f"Reranked {len(ordered_patents)} patents."
        )

        return ordered_patents[:self.TOP_K]