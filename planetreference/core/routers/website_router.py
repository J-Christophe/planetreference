from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/")
async def root():
    return HTMLResponse("Hello!")


# https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864
