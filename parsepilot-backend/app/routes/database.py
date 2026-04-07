from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def database_health() -> dict[str, str]:
	return {"status": "database route ready"}
