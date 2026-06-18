from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.exceptions.auth import AuthException
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register(db: Session, payload: UserCreate) -> User:
        if db.query(User).filter(User.email == payload.email).first():
            raise AuthException("邮箱已注册")
        user = User(
            email=payload.email,
            name=payload.name,
            hashed_password=get_password_hash(payload.password),
            role=payload.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> tuple[str, User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise AuthException("邮箱或密码错误")
        token = create_access_token(str(user.id), {"role": user.role.value})
        return token, user
