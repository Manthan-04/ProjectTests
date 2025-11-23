from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
from core import *

router = APIRouter()
config = Config()
logger =  LogClass(config.LOG_BASE_PATH, config.API_LOGS)

@router.get("/health")
async def health():
    log = await logger.create_logger(logs_for_module="health")
    log.info("Inside the Log Class.")
    return JSONResponse(status_code=200, content={'status': 'ok.'})