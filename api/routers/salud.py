from fastapi import APIRouter

router = APIRouter(prefix= "/salud", tags=["salud"])

@router.get("")
def salud():
    return {
        "estado":
        "ok"
    }