from fastapi import FastAPI, Depends

from routers import api
from auth import auth

from database import engine
from models import *


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api)
app.include_router(auth)


@app.get('/')
async def ping():
    return 'pong'
