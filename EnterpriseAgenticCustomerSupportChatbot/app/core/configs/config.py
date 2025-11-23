import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
    
    LOG_BASE_PATH = os.getenv("LOG_BASE_PATH", "")
    API_LOGS = os.getenv("API_LOGS", "")