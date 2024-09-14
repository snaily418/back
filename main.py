from fastapi import FastAPI, Depends
from routers import api

app = FastAPI()
app.include_router(api)


@app.get('/')
async def ping():
    return 'pong'
