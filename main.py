# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mysql import engine
from models import Base
from routes import data, history, relay, health

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

@app.get("/")
def root():
    return {"message": "Solar Highway Battery API is running"}
