from backend.schemas.state import WorkflowState
from backend.config.settings import logger


class ReportExportTool:

    def export_markdown(self, state: WorkflowState) -> str:

        logger.info("Generating Markdown Report.")

        report = []

        report.append("# PatentMind AI - Patent Research Report\n")

        # ======================================================
        # Executive Summary
        # ======================================================

        if state.strategy_recommendations:

            report.append("## Executive Summary\n")
            report.append(
                state.strategy_recommendations.executive_summary
            )
            report.append("\n")

        # ======================================================
        # User Invention
        # ======================================================

        report.append("## User Invention\n")
        report.append(state.user_invention)
        report.append("\n")

        # ======================================================
        # Research Plan
        # ======================================================

        if state.research_plan:

            report.append("## Research Plan\n")

            report.append(
                f"**Technology Domain:** {state.research_plan.technical_domain}\n"
            )

            report.append("### Important Concepts")

            for concept in state.research_plan.important_concepts:
                report.append(f"- {concept}")

            report.append("\n### Technical Keywords")

            for keyword in state.research_plan.technical_keywords:
                report.append(f"- {keyword}")

            report.append("\n### Search Queries")

            for query in state.research_plan.search_queries:
                report.append(f"- {query}")

            report.append("")

        # ======================================================
        # Patent Intelligence
        # ======================================================

        if state.patent_knowledge:

            report.append("## Patent Intelligence\n")

            for patent in state.patent_knowledge.patents:

                report.append(
                    f"### {patent.title} ({patent.patent_number})"
                )

                report.append(
                    f"**Purpose:** {patent.purpose}"
                )

                report.append(
                    f"**Problem Addressed:** {patent.problem_addressed}"
                )

                report.append(
                    f"**Innovation:** {patent.innovation}"
                )

                report.append(
                    f"**Technologies:** {', '.join(patent.technologies_used)}"
                )

                report.append(
                    f"**Summary:** {patent.summary}"
                )

                report.append(
                    f"**Relevance Score:** {patent.relevance_score}"
                )

                report.append("")

        # ======================================================
        # Novelty Assessment
        # ======================================================

        if state.novelty_assessment:

            novelty = state.novelty_assessment

            report.append("## Novelty Assessment\n")

            report.append(
                f"**Novelty Score:** {novelty.novelty_score}"
            )

            report.append(
                f"**Innovation Score:** {novelty.innovation_score}"
            )

            report.append(
                f"**Overlap Risk:** {novelty.similarity_analysis.overlap_risk}"
            )

            report.append("\n### Existing Features")

            for item in novelty.similarity_analysis.existing_features:
                report.append(f"- {item}")

            report.append("\n### Unique Features")

            for item in novelty.similarity_analysis.unique_features:
                report.append(f"- {item}")

            report.append("\n### Overlap Explanation")

            report.append(
                novelty.overlap_explanation
            )

            report.append("")

        # ======================================================
        # Strategy
        # ======================================================

        if state.strategy_recommendations:

            strategy = state.strategy_recommendations

            report.append("## Strategy Recommendations\n")

            report.append(
                f"### Suggested Patent Title\n{strategy.suggested_patent_title}"
            )

            report.append(
                f"\n### Suggested Abstract\n{strategy.suggested_abstract}"
            )

            report.append("\n### Improvement Suggestions")

            for item in strategy.improvement_suggestions:
                report.append(f"- {item}")

            report.append("\n### Technical Risk Areas")

            for item in strategy.technical_risk_areas:
                report.append(f"- {item}")

            report.append("\n### Future Research Directions")

            for item in strategy.future_research_directions:
                report.append(f"- {item}")

            report.append("")

        return "\n".join(report)