from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio

router = APIRouter()

@router.get("/health")
async def health():
    return JSONResponse(status_code=200, content={'status': 'ok.'})