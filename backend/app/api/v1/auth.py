from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = AuthService.register(db, payload)
    token, user = AuthService.authenticate(db, payload.email, payload.password)
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token, user = AuthService.authenticate(db, payload.email, payload.password)
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
