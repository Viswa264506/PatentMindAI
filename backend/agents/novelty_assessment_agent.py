import json

from backend.agents.base import BaseAgent
from backend.schemas.state import (
    PatentKnowledgeBase,
    NoveltyAssessment,
)
from backend.config.settings import logger
from backend.utils.prompt_formatter import to_json

class NoveltyAssessmentAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            prompt_filename="novelty_assessment_agent.txt",
            name="Novelty Assessment Agent"
        )

    def assess(
        self,
        user_invention: str,
        patent_knowledge: PatentKnowledgeBase
    ) -> NoveltyAssessment:
        """
        Compare the user's invention with the analyzed patent
        knowledge base and estimate novelty.
        """

        logger.info("Novelty Assessment Agent started.")

        if not patent_knowledge.patents:
            logger.warning("Patent knowledge base is empty.")

            return NoveltyAssessment(
                novelty_score=0,
                innovation_score=0,
                overlap_risk="Unknown",
                similarity_analysis={
    "summary": "No patent knowledge available."
},
                unique_features=[],
                existing_features=[],
                reasoning="Novelty assessment could not be performed because no patents were analyzed.",
                confidence_score=0.0
            )

        knowledge_json = to_json(patent_knowledge)

        user_prompt = f"""
User Invention

{user_invention}

Patent Knowledge Base

{knowledge_json}

Instructions

Compare the user's invention with the analyzed patent knowledge.

Identify:

- Existing features
- Unique features
- Technical overlap
- Innovation strength
- Novelty score
- Similarity analysis
- Overlap risk

Return ONLY JSON matching the NoveltyAssessment schema.
"""

        try:

            response = self.execute(
                prompt=user_prompt,
                response_model=NoveltyAssessment
            )

            logger.info(
                "Novelty Assessment Agent completed successfully."
            )

            return response

        except Exception as e:

            logger.exception(
                "Novelty Assessment Agent failed."
            )

            return NoveltyAssessment(
                novelty_score=0,
                innovation_score=0,
                overlap_risk="Unknown",
                similarity_analysis="Novelty assessment failed.",
                unique_features=[],
                existing_features=[],
                reasoning=str(e),
                confidence_score=0.0
            )