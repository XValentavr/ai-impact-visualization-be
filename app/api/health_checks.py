from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter(tags=["healthcheck"])


@router.get("/")
async def health_check()-> Response:
    return Response(status_code=status.HTTP_200_OK, content="OK")
