import uuid
from .database import base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from typing import Literal

class Users(base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class Threads(base):
    __tablename__ = "threads"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Messages(base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String, ForeignKey('threads.id'), nullable=False)
    sender = Column(String, nullable=False)
    message_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
