from backend.agents.base import BaseAgent
from backend.schemas.state import (
    ResearchPlan,
    PatentKnowledgeBase,
    NoveltyAssessment,
    StrategyRecommendations,
)
from backend.config.settings import logger
from backend.utils.prompt_formatter import to_json

class PatentStrategyAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            prompt_filename="patent_strategy_agent.txt",
            name="Patent Strategy Agent"
        )

    def strategize(
        self,
        user_invention: str,
        research_plan: ResearchPlan,
        patent_knowledge: PatentKnowledgeBase,
        novelty_assessment: NoveltyAssessment,
    ) -> StrategyRecommendations:
        """
        Generate strategic recommendations and the final
        patent research report.
        """

        logger.info("Patent Strategy Agent started.")

        plan_json = to_json(research_plan)

        knowledge_json = to_json(patent_knowledge)

        novelty_json = to_json(novelty_assessment)

        user_prompt = f"""
User Invention

{user_invention}

Research Plan

{plan_json}

Patent Knowledge Base

{knowledge_json}

Novelty Assessment

{novelty_json}

Instructions

You are generating the final patent strategy report.

Base every recommendation strictly on:

1. User invention
2. Research Plan
3. Patent Knowledge
4. Novelty Assessment

Do not invent new technologies.

Do not provide legal advice.

Return ONLY valid JSON.
"""

        try:

            response = self.execute(
                prompt=user_prompt,
                response_model=StrategyRecommendations
            )

            logger.info(
                "Patent Strategy Agent completed successfully."
            )

            return response

        except Exception as e:

            logger.exception(
                "Patent Strategy Agent failed."
            )

            return StrategyRecommendations(
                executive_summary="Strategy generation failed.",
                suggested_patent_title="",
                suggested_abstract="",
                improvement_suggestions=[],
                technical_risk_areas=[],
                future_research_directions=[],
                confidence_score=0.0,
                reasoning=str(e)
            )