from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def documents_health() -> dict[str, str]:
	return {"status": "documents route ready"}
