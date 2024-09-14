from sqlalchemy.orm import Session
from passlib.context import CryptContext

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from services.user_service import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth = APIRouter()


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user
