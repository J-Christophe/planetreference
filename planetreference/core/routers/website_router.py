from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/")
async def root():
    return HTMLResponse("Hello!")
