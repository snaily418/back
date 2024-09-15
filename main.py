from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from auth import auth
from database import engine
from models import *
from routers import api
from utils import every_day_check

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api)
app.include_router(auth)


@app.get('/')
async def ping():
    return 'pong'


@app.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=1, minute=0)
    scheduler.add_job(every_day_check, trigger)
    scheduler.start()
