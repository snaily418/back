from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routers import api
from auth import auth

from database import engine
from models import *


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api)
app.include_router(auth)

origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def ping():
    return {"message": "Приложение работает!"}
