from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.deps import get_db
from app.schemas.users import UserCreate, UserLogin, Token, UserResponse
from app.crud.users import (
    get_user_by_email, 
    get_user_by_username,
    create_user, 
    authenticate_user,
    verify_user_email
)
from app.utils.auth import create_access_token
from app.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    """Реєстрація нового користувача"""
    # Перевірка чи користувач вже існує
    if get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    if get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )
    
    # Створення користувача
    db_user = create_user(db=db, user=user)
    
    # TODO: Відправка email для верифікації (додамо пізніше)
    
    return db_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Вхід користувача"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """Верифікація email користувача"""
    if not verify_user_email(db, token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    return {"message": "Email verified successfully"}