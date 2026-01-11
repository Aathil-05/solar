# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# relay_status = "OFF"

# class Data(BaseModel):
#     voltage: float
#     percentage: int
#     current: float

# @app.post("/data")
# def receive_data(d: Data):
#     print("Battery Voltage:", d.voltage)
#     print("Battery %:", d.percentage)
#     print("Current:", d.current)
#     print("Relay:", relay_status)
#     return {"message": "Data received"}

# @app.get("/relay/status")
# def relay_status_api():
#     return relay_status

# @app.get("/relay/on")
# def switch_on():
#     global relay_status
#     relay_status = "ON"
#     return {"status": "Relay ON"}

# @app.get("/relay/off")
# def switch_off():
#     global relay_status
#     relay_status = "OFF"
#     return {"status": "Relay OFF"}


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

# Database setup (SQLite)
# engine = create_engine('mysql+pymysql://root:aathil12@localhost:3306/solardata')
engine = create_engine('mysql+pymysql://root:EabGDkdNYaRXWrMoXyXqQEvivWFtPYWx@centerbeam.proxy.rlwy.net:46194/railway')
Base = declarative_base()

class BatteryData(Base):
    __tablename__ = 'battery_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    voltage = Column(Float)
    percentage = Column(Integer)
    current = Column(Float)
    relay_status = Column(String(10))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Global relay status
relay_status = "OFF"

class Data(BaseModel):
    voltage: float
    percentage: int
    current: float

@app.post("/data")
def receive_data(d: Data):
    global relay_status
    session = Session()
    new_data = BatteryData(voltage=d.voltage, percentage=d.percentage, current=d.current, relay_status=relay_status)
    session.add(new_data)
    session.commit()
    session.close()
    print("Battery Voltage:", d.voltage)
    print("Battery %:", d.percentage)
    print("Current:", d.current)
    print("Relay:", relay_status)
    return {"message": "Data received"}

@app.get("/latest")
def get_latest():
    session = Session()
    latest = session.query(BatteryData).order_by(BatteryData.timestamp.desc()).first()
    session.close()
    if latest:
        return {
            "voltage": latest.voltage,
            "percentage": latest.percentage,
            "current": latest.current,
            "relay": latest.relay_status
        }
    return {"message": "No data available"}

from fastapi import FastAPI, Query
from datetime import datetime, timedelta
from sqlalchemy import desc

@app.get("/history")
def get_history(
    hours: int = Query(None, description="Last N hours"),
    days: int = Query(None, description="Last N days")
):
    session = Session()
    now = datetime.utcnow()

    # Determine time filter
    if hours is not None:
        since = now - timedelta(hours=hours)
    elif days is not None:
        since = now - timedelta(days=days)
    else:
        since = now - timedelta(days=30)  # default fallback

    # Query data
    all_data = session.query(BatteryData)\
        .filter(BatteryData.timestamp >= since)\
        .order_by(BatteryData.timestamp)\
        .all()

    session.close()

    history = []
    for d in all_data:
        sharing_power = round(d.voltage * d.current, 2) if d.relay_status == "ON" else 0.0
        history.append({
            "timestamp": d.timestamp.isoformat(),
            "voltage": round(d.voltage, 2),
            "current": round(d.current, 2),
            "sharing_power": sharing_power,
            "percentage": d.percentage
        })

    return history
@app.get("/relay/status")
def relay_status_api():
    return relay_status

@app.get("/relay/on")
def switch_on():
    global relay_status
    relay_status = "ON"
    return {"status": "Relay ON"}

@app.get("/relay/off")
def switch_off():
    global relay_status
    relay_status = "OFF"
    return {"status": "Relay OFF"}