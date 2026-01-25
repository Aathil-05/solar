# routes/data.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BatteryData
from schemas import BatteryDataCreate, BatteryDataResponse
from routes.relay import get_relay_status

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/", response_model=dict)
def receive_data(data: BatteryDataCreate, db: Session = Depends(get_db)):
    current_relay = get_relay_status()
    
    new_entry = BatteryData(
        voltage=data.voltage,
        percentage=data.percentage,
        current=data.current,
        relay_status=current_relay
    )
    
    db.add(new_entry)
    db.commit()
    
    print(f"Battery Voltage: {data.voltage}")
    print(f"Battery %: {data.percentage}")
    print(f"Current: {data.current}")
    print(f"Relay: {current_relay}")
    
    return {"message": "Data received"}

@router.get("/latest")
def get_latest(db: Session = Depends(get_db)):
    latest = db.query(BatteryData)\
              .order_by(BatteryData.timestamp.desc())\
              .first()

    if not latest:
        return {"message": "No data available"}

    return {
        "voltage": latest.voltage,
        "percentage": latest.percentage,
        "current": latest.current,
        "relay": get_relay_status()  # 🔥 LIVE STATE
    }