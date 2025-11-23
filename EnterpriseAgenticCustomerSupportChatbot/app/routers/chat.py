from fastapi import APIRouter, Request, Header, Query, Path, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal, List, Optional
from core import *

router = APIRouter()
config = Config()
logger =  LogClass(config.LOG_BASE_PATH, config.API_LOGS)

class ChatModel(BaseModel):
    userName: str = Field(description="User name to be provided")
    message: str = Field(description="User message")

@router.post("/chat")
async def chat(request: Request, chat: ChatModel):
    log = await logger.create_logger(logs_for_module="health")
    print(f"The current body is: {chat.model_dump()}")
    log.info(f"The current body is: {chat.model_dump()}")
    return JSONResponse(status_code=200, content={'status': 'ok', 'body': chat.model_dump()})