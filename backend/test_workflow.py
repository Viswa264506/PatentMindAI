from backend.workflow.orchestrator import PatentMindWorkflow


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
    print("PATENTMIND COMPLETE WORKFLOW TEST")
    print("=" * 80)

    workflow = PatentMindWorkflow()

    result = workflow.run(invention)

    print("\n")

    print("=" * 80)
    print("RESEARCH PLAN")
    print("=" * 80)

    if result.research_plan:
        print(result.research_plan.model_dump_json(indent=2))

    print("\n")

    print("=" * 80)
    print(f"RETRIEVED PATENTS ({len(result.retrieved_patents)})")
    print("=" * 80)

    for patent in result.retrieved_patents:
        print(f"Patent Number : {patent.patent_number}")
        print(f"Title         : {patent.title}")
        print(f"Provider      : {patent.provider}")
        print("-" * 80)

    print("\n")

    print("=" * 80)
    print("PATENT KNOWLEDGE")
    print("=" * 80)

    if result.patent_knowledge:
        print(result.patent_knowledge.model_dump_json(indent=2))

    print("\n")

    print("=" * 80)
    print("NOVELTY ASSESSMENT")
    print("=" * 80)

    if result.novelty_assessment:
        print(result.novelty_assessment.model_dump_json(indent=2))

    print("\n")

    print("=" * 80)
    print("PATENT STRATEGY")
    print("=" * 80)

    if result.strategy_recommendations:
        print(result.strategy_recommendations.model_dump_json(indent=2))

    print("\n")

    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    if result.final_report:
        print(result.final_report)
    else:
        print("No report generated.")


if __name__ == "__main__":
    main()