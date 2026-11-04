from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.schemas import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService
from app.services.usage_service import (
    get_usage_summary,
    initialize_usage_db,
    record_usage,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_usage_db()
    yield


app = FastAPI(
    title="VulnVerdict",
    version="0.2.0",
    lifespan=lifespan,
)

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must not call the LLM or DB."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, settings: SettingsDep):
    """Generate an answer and record its token usage."""
    try:
        result = LLMService(settings).generate(request.prompt)

        usage = result["usage"]

        record_usage(
            model=result["model"],
            prompt_tokens=usage["prompt_tokens"],
            response_tokens=usage["response_tokens"],
            thoughts_tokens=usage["thoughts_tokens"],
            total_tokens=usage["total_tokens"],
        )

        return GenerateResponse(
            answer=result["answer"],
            model=result["model"],
            prompt_tokens=usage["prompt_tokens"],
            response_tokens=usage["response_tokens"],
            total_tokens=usage["total_tokens"],
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail="All configured LLM models failed",
        ) from exc


@app.get("/usage")
def usage():
    """Return aggregated LLM usage statistics."""
    return get_usage_summary()
