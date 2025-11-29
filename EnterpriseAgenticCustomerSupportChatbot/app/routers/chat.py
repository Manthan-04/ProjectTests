from fastapi import APIRouter, Request, Header, Query, Path, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal, List, Optional
from core import *

# Table names are shown as below.
# Users, Threads, Messages

router = APIRouter()
config = Config()
logger =  LogClass(config.LOG_BASE_PATH, config.API_LOGS)
database = DBTransaction()
conversation = Conversation()

class ChatModel(BaseModel):
    userName: str = Field(description="User name to be provided")
    userEmail: str = Field(description="User name to be provided")
    message: str = Field(description="User message")
    title: str = Field(description="Title of the conversation.")
    thread_id: Optional[str] = Field(None, description="Title of the conversation.")

class Response(BaseModel):
    status: int
    detail: str
    message: str

@router.post("/chat", response_model=Response)
async def chat(request: Request, chat: ChatModel, db: database.get_cnx()):
    log = await logger.create_logger(logs_for_module="chat")
    body = chat.model_dump()

    thread_id = body.get("thread_id", "")
    userEmail = body.get('userEmail', '')
    userMessage = body.get("message", "")
    log.info(f"User: {userEmail} -- Thread: {thread_id}.")

    params = {}
    params['table'], params['columns'], params['values'] = Users, Users.email, userEmail
    log.info(f"User: {userEmail} -- Thread: {thread_id}. Checking if user is already present or not: {params}")
    userDetails = await database.view(db, params)
    log.info(f"User: {userEmail} -- Thread: {thread_id}. User details are: {userDetails}")

    if not userDetails:
        log.info(f"User: {userEmail} -- Thread: {thread_id}. User not present. Creating the user: {userEmail}")
        createUser = Users(name = body.get("userName", ""), email = userEmail)
        db.add(createUser)
        db.commit()
        
        userDetails = await database.view(db, params)
        if not userDetails:
            log.info(f"User: {userEmail} -- Thread: {thread_id}. User creation failed.")
            return JSONResponse(status_code=500, content={'status': 500, 'detail': 'Internal Server Error.', 'message': 'User creation failed'})
        else:
            log.info(f"User: {userEmail} -- Thread: {thread_id}. User creation result: {userDetails.email}. Now creating user conversation thread.")
            createThread = Threads(user_id = userDetails.id, title = body.get("title", ""))
            db.add(createThread)
            db.commit()

            params = {}
            params['table'], params['columns'], params['values'] = Threads, Threads.user_id, userDetails.id
            log.info(f"User: {userEmail} -- Thread: {thread_id}. Checking the conversation thread details: {params}")
            threadResult = await database.view(db, params)
            thread_id = threadResult.id
            log.info(f"User: {userEmail} -- Thread: {thread_id}. Conversation thread id is: {thread_id}")

    if thread_id:
        log.info(f"User: {userEmail} -- Thread: {thread_id}. Storing the message.")
        createMessage = Messages(thread_id = thread_id, sender = "USER", message_text = userMessage)
        db.add(createMessage)
        db.commit()
        if createMessage:
            log.info(f"User: {userEmail} -- Thread: {thread_id}. Message stored successfully which is: {userMessage[:20]}...")
            modelResponse = conversation.modelResponse(userMessage)
            createMessage = Messages(thread_id = thread_id, sender = modelResponse["role"], message_text = modelResponse["content"])
            db.add(createMessage)
            db.commit()
            log.info(f"User: {userEmail} -- Thread: {thread_id}. AI Message is: {modelResponse['content'][:20]}...")
            return JSONResponse(status_code=200, content= {'status': 200, 'detail': 'ok', 'message': modelResponse['content'], 'thread_id': thread_id})
        else:
            log.info(f"User: {userEmail} -- Thread: {thread_id}. Message storing Failed.")
            return JSONResponse(status_code=400, content= {'status': 400, 'detail': 'Internal Server Error.', 'message': 'Message Save Failed.'})
    else:
        log.info(f"User: {userEmail} -- Thread: {thread_id}. User creation faied / If user already exists thread_id not provided.")
        return JSONResponse(status_code=400, content={'status': 400, 'detail': "Internal Server Error.", 'message': 'User creation faied / If user already exists thread_id not provided.'})