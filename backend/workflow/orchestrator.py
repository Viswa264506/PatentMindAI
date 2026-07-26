from backend.schemas.state import WorkflowState
from backend.agents.research_planning_agent import ResearchPlanningAgent
from backend.agents.patent_intelligence_agent import PatentIntelligenceAgent
from backend.agents.novelty_assessment_agent import NoveltyAssessmentAgent
from backend.agents.patent_strategy_agent import PatentStrategyAgent

from backend.services.patent_search_service import PatentSearchService
from backend.tools.report_export_tool import ReportExportTool

from backend.config.settings import logger

import traceback
import time


class PatentMindWorkflow:

    def __init__(self):

        self.research_agent = ResearchPlanningAgent()
        self.intelligence_agent = PatentIntelligenceAgent()
        self.novelty_agent = NoveltyAssessmentAgent()
        self.strategy_agent = PatentStrategyAgent()

        self.search_service = PatentSearchService()
        self.export_tool = ReportExportTool()

    def run(self, user_invention: str) -> WorkflowState:
        """
        Execute the complete multi-agent workflow.
        """

        logger.info("=" * 70)
        logger.info("PatentMind Workflow Started")
        logger.info("=" * 70)

        start_time = time.time()

        state = WorkflowState(
            user_invention=user_invention
        )

        try:

            # --------------------------------------------------
            # Phase 1
            # --------------------------------------------------

            logger.info("Phase 1 : Research Planning")

            state.research_plan = self.research_agent.plan(
                state.user_invention
            )

            # --------------------------------------------------
            # Phase 2
            # --------------------------------------------------

            logger.info("Phase 2 : Patent Retrieval")

            state.retrieved_patents = (
                self.search_service.execute_search_strategy(
                    user_invention=state.user_invention,
                    research_plan=state.research_plan
                )
            )

            if not state.retrieved_patents:
                raise ValueError(
                    "No patents retrieved."
                )

            logger.info(
                f"{len(state.retrieved_patents)} patents retrieved."
            )

            # --------------------------------------------------
            # Phase 3
            # --------------------------------------------------

            logger.info("Phase 3 : Patent Intelligence")

            state.patent_knowledge = (
                self.intelligence_agent.analyze(
                    state.research_plan,
                    state.retrieved_patents
                )
            )

            # --------------------------------------------------
            # Phase 4
            # --------------------------------------------------

            logger.info("Phase 4 : Novelty Assessment")

            state.novelty_assessment = (
                self.novelty_agent.assess(
                    state.user_invention,
                    state.patent_knowledge
                )
            )

            # --------------------------------------------------
            # Phase 5
            # --------------------------------------------------

            logger.info("Phase 5 : Patent Strategy")

            state.strategy_recommendations = (
                self.strategy_agent.strategize(
                    state.user_invention,
                    state.research_plan,
                    state.patent_knowledge,
                    state.novelty_assessment
                )
            )

            # --------------------------------------------------
            # Phase 6
            # --------------------------------------------------

            logger.info("Phase 6 : Report Generation")

            state.final_report = (
                self.export_tool.export_markdown(
                    state
                )
            )

            elapsed = round(
                time.time() - start_time,
                2
            )

            logger.info(
                f"Workflow completed successfully in {elapsed} seconds."
            )

        except Exception as e:

            logger.exception(
                "Workflow execution failed."
            )

            state.error = str(e)

        logger.info("=" * 70)

        return state