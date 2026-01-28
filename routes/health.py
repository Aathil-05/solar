from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.api_route("/", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}
