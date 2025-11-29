from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core import *
from routers import health, chat

app = FastAPI()
config = Config()
logger =  LogClass(config.LOG_BASE_PATH, config.API_LOGS)

app.include_router(health.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.middleware('http')
async def middleware(request: Request, call_next):
    return await call_next(request)

@app.get("/")
async def baseFunc():
    return JSONResponse(status_code=200, content={'status': 'ok.'})

@app.on_event('startup')
async def startup_event():
    base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def globalExceptionHandler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "detail": "Internal Server Error.",
            "error": str(exc)
        }
    )