from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message (same role as notebook EntryBox text)")


class ChatResponse(BaseModel):
    answer: str
    alternate: int | float
    qid: int
    aid: int


class HealthResponse(BaseModel):
    status: str
