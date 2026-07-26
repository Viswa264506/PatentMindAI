from typing import List, Optional
from pydantic import BaseModel, Field


# ==========================================================
# Base Agent Output
# ==========================================================

class AgentOutputBase(BaseModel):
    confidence_score: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    reasoning: Optional[str] = ""


# ==========================================================
# Research Planning
# ==========================================================

class ResearchPlan(AgentOutputBase):

    invention_summary: str

    technical_domain: str

    important_concepts: List[str]

    search_queries: List[str]

    technical_keywords: List[str]

    research_focus: str


# ==========================================================
# Patent Search
# ==========================================================

class Patent(BaseModel):

    patent_number: str

    title: str

    abstract: str

    url: Optional[str] = None

    provider: str

class PatentRanking(BaseModel):
    
    patent_numbers: List[str]


# ==========================================================
# Patent Intelligence
# ==========================================================

class PatentIntelligence(BaseModel):

    patent_number: str

    title: str

    purpose: str

    problem_addressed: str

    technologies_used: List[str]

    innovation: str

    key_claims: List[str]

    summary: str

    relevance_score: float = Field(
        ge=0,
        le=100
    )


class PatentKnowledgeBase(AgentOutputBase):

    patents: List[PatentIntelligence] = Field(default_factory=list)


# ==========================================================
# Novelty Assessment
# ==========================================================

class SimilarityAnalysis(BaseModel):

    existing_features: List[str] = Field(default_factory=list)

    unique_features: List[str] = Field(default_factory=list)

    overlap_risk: str


class NoveltyAssessment(AgentOutputBase):

    similarity_analysis: SimilarityAnalysis

    novelty_score: int = Field(
        ge=0,
        le=100
    )

    innovation_score: int = Field(
        ge=0,
        le=100
    )

    overlap_explanation: str


# ==========================================================
# Strategy Recommendations
# ==========================================================

class StrategyRecommendations(AgentOutputBase):

    executive_summary: str

    suggested_patent_title: str

    suggested_abstract: str

    improvement_suggestions: List[str] = Field(default_factory=list)

    technical_risk_areas: List[str] = Field(default_factory=list)

    future_research_directions: List[str] = Field(default_factory=list)


# ==========================================================
# Workflow State
# ==========================================================

class WorkflowState(BaseModel):

    user_invention: str

    research_plan: Optional[ResearchPlan] = None

    retrieved_patents: List[Patent] = Field(default_factory=list)

    patent_knowledge: Optional[PatentKnowledgeBase] = None

    novelty_assessment: Optional[NoveltyAssessment] = None

    strategy_recommendations: Optional[StrategyRecommendations] = None

    final_report: Optional[str] = None

    current_phase: str = "Initialized"

    status: str = "Running"

    error: Optional[str] = None