# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:aathil12@localhost:3306/solardata"
)

# DATABASE_URL = os.getenv("DATABASE_URL", 
#     "mysql+pymysql://solar_highwayhow:7b0e3ba3b8fcff9bfefcab1e11e659e0f7465375@fu5ryk.h.filess.io:3307/solar_highwayhow")

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()