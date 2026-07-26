from backend.agents.base import BaseAgent
from backend.schemas.state import ResearchPlan
from backend.config.settings import logger


class ResearchPlanningAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            prompt_filename="research_planning_agent.txt",
            name="Research Planning Agent"
        )

    def plan(self, user_invention: str) -> ResearchPlan:

        logger.info("Research Planning Agent started.")

        user_prompt = f"""
User Invention

{user_invention}

Instructions

Analyze the invention and generate:

- invention_summary
- technical_domain
- important_concepts
- technical_keywords
- search_queries
- research_focus

Return ONLY JSON matching the ResearchPlan schema.
"""

        result = self.execute(
            prompt=user_prompt,
            response_model=ResearchPlan
        )

        logger.info("Research Planning Agent completed.")

        return result