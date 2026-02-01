# routes/data.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BatteryData
from schemas import BatteryDataCreate
from routes.relay import all_relay_status

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/", response_model=dict)
def receive_data(data: BatteryDataCreate, db: Session = Depends(get_db)):
    relays = all_relay_status()

    new_entry = BatteryData(
        voltage=data.voltage,
        percentage=data.percentage,
        current=data.current,
        relay_home=relays["home"],
        relay_neighbour=relays["neighbour"],
        relay_solar=relays["solar"],
    )

    db.add(new_entry)
    db.commit()

    return {"message": "Data received successfully"}

@router.get("/latest")
def get_latest(db: Session = Depends(get_db)):
    latest = (
        db.query(BatteryData)
        .order_by(BatteryData.timestamp.desc())
        .first()
    )

    relays = all_relay_status()  # LIVE STATE

    if not latest:
        return {
            "voltage": 0,
            "percentage": 0,
            "current": 0,
            "relay": relays
        }

    return {
        "voltage": latest.voltage,
        "percentage": latest.percentage,
        "current": latest.current,
        "relay": relays
    }
