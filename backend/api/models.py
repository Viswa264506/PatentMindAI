from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    invention: str


class AnalyzeResponse(BaseModel):
    success: bool
    message: str
    result: dict