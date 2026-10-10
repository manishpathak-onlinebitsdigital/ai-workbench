"""
AI Workbench API — FastAPI application.
Routing layer only: receives requests, delegates to services, returns responses.
"""

from fastapi import FastAPI, HTTPException
from .models import TextRequest, TextResponse, HealthResponse
from .services import process_task
from .llm_client import get_provider_info

app = FastAPI(
    title="AI Workbench API",
    description="A multi-task LLM-powered text processing service",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    info = get_provider_info()
    return HealthResponse(status="healthy", **info)


@app.post("/summarize", response_model=TextResponse)
def summarize(req: TextRequest):
    return _handle_task("summarize", req.text)


@app.post("/rewrite", response_model=TextResponse)
def rewrite(req: TextRequest):
    return _handle_task("rewrite", req.text)


@app.post("/keypoints", response_model=TextResponse)
def keypoints(req: TextRequest):
    return _handle_task("keypoints", req.text)


@app.post("/explain", response_model=TextResponse)
def explain(req: TextRequest):
    return _handle_task("explain", req.text)


def _handle_task(task: str, text: str) -> TextResponse:
    try:
        result = process_task(task, text)
        info = get_provider_info()
        return TextResponse(
            task=result["task"],
            result=result["content"],
            model=info["model"],
            tokens_used=result["tokens_used"],
        )
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
