# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mysql import engine
from models import Base
from routes import data, history, relay, health
from apscheduler.schedulers.background import BackgroundScheduler
from ml.auto_job import auto_ml_job
from firebase import firebase_service

app = FastAPI(title="Solar Highway Battery Monitoring API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
app.include_router(history.router)
app.include_router(relay.router)
app.include_router(health.router)
app.include_router(firebase_service.router)

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(
        auto_ml_job,
        trigger="cron",
        minute=0   # runs at HH:00 every hour
    )
    scheduler.start()



@app.get("/")
def root():
    return {"message": "Solar Highway Battery API is running"}
