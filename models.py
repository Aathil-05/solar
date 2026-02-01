# models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from mysql import Base

class BatteryData(Base):
    __tablename__ = "battery_data"

    id = Column(Integer, primary_key=True, index=True)
    voltage = Column(Float, default=0)
    current = Column(Float, default=0)
    percentage = Column(Float, default=0)

    relay_home = Column(String, default="OFF")
    relay_neighbour = Column(String, default="OFF")
    relay_solar = Column(String, default="OFF")

    timestamp = Column(DateTime, default=datetime.utcnow)
