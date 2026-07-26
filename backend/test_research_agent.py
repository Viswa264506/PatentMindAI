from backend.agents.research_planning_agent import ResearchPlanningAgent

agent = ResearchPlanningAgent()

result = agent.plan(
    """
    An AI-powered smart helmet that detects accidents using sensors,
    sends GPS location to emergency contacts,
    and predicts worker fatigue using machine learning.
    """
)

print(result.model_dump_json(
    exclude_none=True,
    indent=2
))