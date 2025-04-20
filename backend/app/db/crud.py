# backend/app/db/crud.py
from sqlalchemy.orm import Session
from app.db.models import User, Space, Content, Generation
from app.auth.security import get_password_hash

# User CRUD operations
def create_user(db: Session, name: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(name=name, email=email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

# Space CRUD operations
def create_space(db: Session, name: str, description: str, user_id: str):
    db_space = Space(name=name, description=description, user_id=user_id)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space

def get_spaces_by_user(db: Session, user_id: str):
    return db.query(Space).filter(Space.user_id == user_id).all()

def get_space_by_id(db: Session, space_id: str):
    return db.query(Space).filter(Space.id == space_id).first()

def update_space(db: Session, space_id: str, name: str = None, description: str = None):
    db_space = get_space_by_id(db, space_id)
    if db_space:
        if name:
            db_space.name = name
        if description:
            db_space.description = description
        db.commit()
        db.refresh(db_space)
    return db_space

def delete_space(db: Session, space_id: str):
    db_space = get_space_by_id(db, space_id)
    if db_space:
        db.delete(db_space)
        db.commit()
        return True
    return False

# Content CRUD operations
def create_content(db: Session, title: str, type: str, data: dict, space_id: str):
    db_content = Content(title=title, type=type, data=data, space_id=space_id)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_content_by_id(db: Session, content_id: str):
    return db.query(Content).filter(Content.id == content_id).first()

def get_contents_by_space(db: Session, space_id: str):
    return db.query(Content).filter(Content.space_id == space_id).all()

def delete_content(db: Session, content_id: str):
    db_content = get_content_by_id(db, content_id)
    if db_content:
        db.delete(db_content)
        db.commit()
        return True
    return False

# Generation CRUD operations
def create_generation(db: Session, type: str, data: dict, content_id: str):
    db_generation = Generation(type=type, data=data, content_id=content_id)
    db.add(db_generation)
    db.commit()
    db.refresh(db_generation)
    return db_generation

def get_generations_by_content(db: Session, content_id: str, generation_type: str = None):
    query = db.query(Generation).filter(Generation.content_id == content_id)
    if generation_type:
        query = query.filter(Generation.type == generation_type)
    return query.all()