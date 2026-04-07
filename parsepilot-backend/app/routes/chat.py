from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def chat_health() -> dict[str, str]:
	return {"status": "chat route ready"}
