# backend/app/api/routes/generate.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.db.crud import (
    get_content_by_id, create_generation, get_generations_by_content
)
from app.auth.security import get_current_user
from app.services.generate.summary import generate_summary
from app.services.generate.chat import generate_chat_response
from app.services.generate.flashcard import generate_flashcards
from app.services.generate.mindmap import generate_mindmap
from app.services.generate.quiz import generate_quiz
from app.db.models import User

router = APIRouter()

class GenerationRequest(BaseModel):
    content_id: str
    prompt: Optional[str] = None

class ChatRequest(BaseModel):
    content_id: str
    message: str
    history: Optional[List[dict]] = None

class GenerationResponse(BaseModel):
    id: str
    type: str
    data: dict

@router.post("/summary", response_model=GenerationResponse)
async def create_summary(
    data: GenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = get_content_by_id(db, content_id=data.content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Verify the user has access to this content
    if content.space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this content"
        )
    
    # Check if we already have a summary for this content
    existing_summaries = get_generations_by_content(db, content_id=content.id, generation_type="summary")
    if existing_summaries:
        return {
            "id": existing_summaries[0].id,
            "type": "summary",
            "data": existing_summaries[0].data
        }
    
    # Get raw text from content
    raw_text = ""
    if content.type == "youtube":
        raw_text = content.data.get("transcript", "")
    
    # Generate summary
    summary = generate_summary(raw_text)
    
    # Save generation
    generation = create_generation(
        db,
        type="summary",
        data={"summary": summary},
        content_id=content.id
    )
    
    return {
        "id": generation.id,
        "type": generation.type,
        "data": generation.data
    }

@router.post("/chat", response_model=GenerationResponse)
async def chat_with_content(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = get_content_by_id(db, content_id=data.content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Verify the user has access to this content
    if content.space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this content"
        )
    
    # Get raw text from content
    content_text = ""
    if content.type == "youtube":
        content_text = content.data.get("transcript", "")
    
    # Generate chat response
    response = generate_chat_response(content_text, data.message, data.history)
    
    # We're not saving chat messages to the database in this implementation
    # Just returning the response directly
    
    return {
        "id": "chat_response",
        "type": "chat",
        "data": {
            "message": data.message,
            "response": response,
            "timestamp": "now"
        }
    }

@router.post("/flashcard", response_model=GenerationResponse)
async def create_flashcards(
    data: GenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = get_content_by_id(db, content_id=data.content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Verify the user has access to this content
    if content.space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this content"
        )
    
    # # Check if we already have flashcards for this content
    # COON WAS HERE AND YAHA ISSUE H      CLAUDE NE PURA NAHI KARKE DIA ACHE SE
    # existing_flashcards = get_generations_by_content(db, content_id=content.id, generation_type="flashcard")
    # if existing_flashcards:
    #     return {
    #         "id": existing_flashcards[0k]
    #     }