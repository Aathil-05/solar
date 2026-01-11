from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allow all (or add your web app URL later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)