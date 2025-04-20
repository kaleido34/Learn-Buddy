# backend/app/api/routes/spaces.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.db.crud import (
    create_space, get_spaces_by_user, get_space_by_id, 
    update_space, delete_space, get_contents_by_space
)
from app.auth.security import get_current_user
from app.db.models import User

router = APIRouter()

class SpaceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SpaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ContentBase(BaseModel):
    id: str
    title: str
    type: str
    created_at: str

class SpaceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    contents: List[ContentBase] = []

@router.post("", response_model=SpaceResponse)
async def create_new_space(
    space_data: SpaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    space = create_space(
        db, 
        name=space_data.name,
        description=space_data.description,
        user_id=current_user.id
    )
    
    return {
        "id": space.id,
        "name": space.name,
        "description": space.description,
        "contents": []
    }

@router.get("", response_model=List[SpaceResponse])
async def get_user_spaces(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    spaces = get_spaces_by_user(db, user_id=current_user.id)
    
    result = []
    for space in spaces:
        contents = get_contents_by_space(db, space_id=space.id)
        content_list = [
            {
                "id": content.id,
                "title": content.title,
                "type": content.type,
                "created_at": content.created_at.isoformat()
            }
            for content in contents
        ]
        
        result.append({
            "id": space.id,
            "name": space.name,
            "description": space.description,
            "contents": content_list
        })
    
    return result

@router.get("/{space_id}", response_model=SpaceResponse)
async def get_space(
    space_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    space = get_space_by_id(db, space_id=space_id)
    
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space not found"
        )
    
    if space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this space"
        )
    
    contents = get_contents_by_space(db, space_id=space.id)
    content_list = [
        {
            "id": content.id,
            "title": content.title,
            "type": content.type,
            "created_at": content.created_at.isoformat()
        }
        for content in contents
    ]
    
    return {
        "id": space.id,
        "name": space.name,
        "description": space.description,
        "contents": content_list
    }

@router.put("/{space_id}", response_model=SpaceResponse)
async def update_space_details(
    space_id: str,
    space_data: SpaceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    space = get_space_by_id(db, space_id=space_id)
    
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space not found"
        )
    
    if space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this space"
        )
    
    updated_space = update_space(
        db,
        space_id=space_id,
        name=space_data.name,
        description=space_data.description
    )
    
    contents = get_contents_by_space(db, space_id=space.id)
    content_list = [
        {
            "id": content.id,
            "title": content.title,
            "type": content.type,
            "created_at": content.created_at.isoformat()
        }
        for content in contents
    ]
    
    return {
        "id": updated_space.id,
        "name": updated_space.name,
        "description": updated_space.description,
        "contents": content_list
    }

@router.delete("/{space_id}")
async def delete_user_space(
    space_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    space = get_space_by_id(db, space_id=space_id)
    
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space not found"
        )
    
    if space.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this space"
        )
    
    delete_space(db, space_id=space_id)
    
    return {"message": "Space deleted successfully"}