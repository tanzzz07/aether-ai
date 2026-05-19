import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.config import Settings, get_settings
from backend.models import GenerationRequest, GenerationResult
from backend.orchestrator.generation_graph import GenerationOrchestrator
from backend.services.ai_provider import AIProvider
from backend.services.auth import AuthUser, get_current_user

router = APIRouter(prefix="/generation", tags=["generation"])

def get_orchestrator(settings: Settings = Depends(get_settings)) -> GenerationOrchestrator:
    return GenerationOrchestrator(AIProvider(settings))

@router.post("", response_model=GenerationResult)
async def generate(
    request: GenerationRequest,
    user: AuthUser = Depends(get_current_user),
    orchestrator: GenerationOrchestrator = Depends(get_orchestrator),
) -> GenerationResult:
    _ = user
    return await orchestrator.run(request.prompt)

@router.post("/stream")
async def stream_generation(
    request: GenerationRequest,
    user: AuthUser = Depends(get_current_user),
    orchestrator: GenerationOrchestrator = Depends(get_orchestrator),
) -> StreamingResponse:
    _ = user

    async def events():
        async for event in orchestrator.stream(request.prompt):
            yield f"event: {event.step}\ndata: {json.dumps(event.model_dump())}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")