# backend/app/api/routes/contents.py
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.db.crud import (
    create_content, get_content_by_id, get_contents_by_space,
    delete_content, get_space_by_id
)
from app.auth.security import get_current_user
from app.services.youtube_service import extract_youtube_info
from app.db.models import User
import json

router = APIRouter()

class YouTubeRequest(BaseModel):
    url: str
    space_id: str

class ContentResponse(BaseModel):
    id: str
    title: str
    type: str
    data: dict
    space_id: str

@router.post("/youtube", response_model=ContentResponse)
async def process_youtube_content(
    data: YouTubeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify the space exists and belongs to the user
    space = get_space_by_id(db, space_id=data.space_id)
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space not found"
        )
    
    if space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add content to this space"
        )
    
    try:
        # Extract YouTube info
        youtube_data = extract_youtube_info(data.url)
        
        # Create content
        content = create_content(
            db,
            title=youtube_data["title"],
            type="youtube",
            data=youtube_data,
            space_id=data.space_id
        )
        
        return {
            "id": content.id,
            "title": content.title,
            "type": content.type,
            "data": content.data,
            "space_id": content.space_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing YouTube URL: {str(e)}"
        )

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = get_content_by_id(db, content_id=content_id)
    
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
    
    return {
        "id": content.id,
        "title": content.title,
        "type": content.type,
        "data": content.data,
        "space_id": content.space_id
    }

@router.delete("/{content_id}")
async def remove_content(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = get_content_by_id(db, content_id=content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Verify the user has access to this content
    if content.space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this content"
        )
    
    delete_content(db, content_id=content_id)
    
    return {"message": "Content deleted successfully"}