"""Request and response models. Empty for now; you add these from Session 4."""

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)


class GenerateResponse(BaseModel):
    answer: str
    model: str
    prompt_tokens: int
    response_tokens: int
    total_tokens: int
