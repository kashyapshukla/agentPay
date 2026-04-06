from fastapi import APIRouter

router = APIRouter(prefix="/v1/gateway", tags=["gateway"])

@router.get("/status")
async def gateway_status():
    return {"status": "ok", "message": "Gateway routing active"}
