# backend/app/db/models.py
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    spaces = relationship("Space", back_populates="user", cascade="all, delete-orphan")

class Space(Base):
    __tablename__ = "spaces"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="spaces")
    contents = relationship("Content", back_populates="space", cascade="all, delete-orphan")

class Content(Base):
    __tablename__ = "contents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "youtube", "document", "audio"
    data = Column(JSON, nullable=False)
    space_id = Column(String, ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    space = relationship("Space", back_populates="contents")
    generations = relationship("Generation", back_populates="content", cascade="all, delete-orphan")

class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)  # "chat", "summary", "flashcard", "mindmap", "quiz"
    data = Column(JSON, nullable=False)
    content_id = Column(String, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    content = relationship("Content", back_populates="generations")