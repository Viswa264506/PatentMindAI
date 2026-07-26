from fastapi import APIRouter, HTTPException

from backend.api.models import (
    AnalyzeRequest,
    AnalyzeResponse
)

from backend.workflow.orchestrator import PatentMindWorkflow


router = APIRouter()

workflow = PatentMindWorkflow()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze(request: AnalyzeRequest):

    try:

        result = workflow.run(request.invention)

        return AnalyzeResponse(
            success=True,
            message="Patent analysis completed successfully.",
            result=result.model_dump()
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )