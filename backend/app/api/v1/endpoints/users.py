import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(User).all()

# Get the current user
@router.get("/me", response_model=UserResponse)
def get_auth_user(current_user: User = Depends(get_current_user)):
    return current_user
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
    
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: uuid.UUID, updated_user: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Solo actualizar los campos que vienen
    if updated_user.email is not None:
        # validar que no exista otro con ese email
        user.email = updated_user.email
        
    if updated_user.username is not None:
        user.username = updated_user.username
    
    if updated_user.password is not None:
        user.password = updated_user.password
    
    db.commit()
    db.refresh(user)
    return user   