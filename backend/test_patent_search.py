from backend.agents.research_planning_agent import ResearchPlanningAgent
from backend.services.patent_search_service import PatentSearchService

agent = ResearchPlanningAgent()
service = PatentSearchService()

plan = agent.plan(
    """
    An AI-powered smart helmet that detects accidents using sensors,
    sends GPS location to emergency contacts,
    and predicts worker fatigue using machine learning.
    """
)

print("=" * 80)
print("SEARCH QUERIES")
print("=" * 80)

print(plan.search_queries)

print("\nSearching patents...\n")

patents = service.execute_search_strategy(plan)

print(f"Retrieved {len(patents)} patents\n")

for patent in patents:
    print("=" * 60)
    print("Patent Number :", patent.patent_number)
    print("Title         :", patent.title)
    print("Provider      :", patent.provider)
    print()