import uvicorn

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import auth
from database import engine, session
from models import *
from routers import api
from services.every_service import every_day_check

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
    return 'pong'


@app.on_event("startup")
def startup_event():
    db = session()

    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=1, minute=0)
    scheduler.add_job(every_day_check, trigger, args=(db,))
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
