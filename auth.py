from typing import Annotated
from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError
from utils import get_password_hash, verify_password

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import schemas
from database import get_db
from services.user_service import get_user_by_name, get_user, create_user

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth = APIRouter()


class TokenData(BaseModel):
    user_id: int


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Annotated[Session, Depends(get_db)],
                           token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not auth",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception

    return user


@auth.post('/token')
async def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> schemas.Token:
    user = authenticate_user(db, credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")


@auth.post('/register')
async def register(credentials: schemas.UserCreateOrUpdate, db: Annotated[Session, Depends(get_db)]) -> schemas.Token:
    user = create_user(credentials)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")
