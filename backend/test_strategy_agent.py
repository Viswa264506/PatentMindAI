from backend.agents.research_planning_agent import ResearchPlanningAgent
from backend.agents.patent_intelligence_agent import PatentIntelligenceAgent
from backend.agents.novelty_assessment_agent import NoveltyAssessmentAgent
from backend.agents.patent_strategy_agent import PatentStrategyAgent
from backend.services.patent_search_service import PatentSearchService


def main():

    invention = """
    AI powered smart helmet for construction workers.

    Features:
    - Accident detection
    - GPS tracking
    - Emergency contact notification
    - Worker fatigue detection using machine learning
    """

    print("=" * 80)
    print("STEP 1 : Research Planning")
    print("=" * 80)

    research_agent = ResearchPlanningAgent()
    research_plan = research_agent.plan(invention)

    print("✅ Research Plan Generated\n")

    print("=" * 80)
    print("STEP 2 : Semantic Patent Search")
    print("=" * 80)

    search_service = PatentSearchService()
    patents = search_service.execute_search_strategy(research_plan)

    print(f"✅ Retrieved {len(patents)} patents\n")

    print("=" * 80)
    print("STEP 3 : Patent Intelligence")
    print("=" * 80)

    intelligence_agent = PatentIntelligenceAgent()

    patent_knowledge = intelligence_agent.analyze(
        research_plan,
        patents
    )

    print("✅ Patent Knowledge Generated\n")

    print("=" * 80)
    print("STEP 4 : Novelty Assessment")
    print("=" * 80)

    novelty_agent = NoveltyAssessmentAgent()

    novelty = novelty_agent.assess(
        user_invention=invention,
        patent_knowledge=patent_knowledge
    )

    print("✅ Novelty Assessment Generated\n")

    print("=" * 80)
    print("STEP 5 : Patent Strategy")
    print("=" * 80)

    strategy_agent = PatentStrategyAgent()

    strategy = strategy_agent.strategize(
        user_invention=invention,
        research_plan=research_plan,
        patent_knowledge=patent_knowledge,
        novelty_assessment=novelty
    )

    print("✅ Strategy Generated\n")

    print("=" * 80)
    print("PATENT STRATEGY REPORT")
    print("=" * 80)

    print(
        strategy.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()