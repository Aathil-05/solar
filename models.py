# models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from mysql import Base

class BatteryData(Base):
    __tablename__ = "battery_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    voltage = Column(Float)
    percentage = Column(Integer)
    current = Column(Float)
    relay_status = Column(String(10))