from typing import List
import json

from backend.agents.base import BaseAgent
from backend.schemas.state import (
    ResearchPlan,
    Patent,
    PatentKnowledgeBase,
)
from backend.config.settings import logger
from backend.utils.prompt_formatter import to_json

class PatentIntelligenceAgent(BaseAgent):

    MAX_PATENTS = 8

    def __init__(self):
        super().__init__(
            prompt_filename="patent_intelligence_agent.txt",
            name="Patent Intelligence Agent"
        )

    def analyze(
        self,
        research_plan: ResearchPlan,
        retrieved_patents: List[Patent]
    ) -> PatentKnowledgeBase:
        """
        Analyze retrieved patents and convert them into
        structured patent knowledge.
        """

        logger.info("Patent Intelligence Agent started.")

        if not retrieved_patents:
            logger.warning("No patents received for analysis.")

            return PatentKnowledgeBase(
                patents=[],
                confidence_score=0.0,
                reasoning="No patents were available for analysis."
            )

        # Limit patents to avoid excessive token usage
        patents = retrieved_patents[: self.MAX_PATENTS]

        logger.info(
            f"Analyzing {len(patents)} patent(s)."
        )

        research_plan_json = to_json(research_plan)

        patents_json = to_json(patents)

        

        user_prompt = f"""
Research Plan

{research_plan_json}

Retrieved Patents

{patents_json}

Instructions

Analyze every patent independently.

For each patent identify:

- Purpose
- Problem Addressed
- Technologies Used
- Main Innovation
- Key Technical Claims (if available)
- Technical Summary
- Relevance Score
- Confidence Score
- Reasoning

Do NOT compare patents.

Do NOT estimate novelty.

Do NOT recommend improvements.

Return ONLY JSON matching the PatentKnowledgeBase schema.
"""

        try:

            response = self.execute(
                prompt=user_prompt,
                response_model=PatentKnowledgeBase
            )

            logger.info(
                "Patent Intelligence Agent completed successfully."
            )

            return response

        except Exception as e:

            logger.exception(
                "Patent Intelligence Agent failed."
            )

            return PatentKnowledgeBase(
                patents=[],
                confidence_score=0.0,
                reasoning=f"Patent analysis failed: {str(e)}"
            )