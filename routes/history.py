# routes/history.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import BatteryData

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=list[dict])
def get_history(
    hours: int = Query(0, description="Last N hours"),
    days: int = Query(0, description="Last N days"),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()

    if hours > 0:
        since = now - timedelta(hours=hours)
    elif days > 0:
        since = now - timedelta(days=days)
    else:
        since = now - timedelta(days=30)

    data = (
        db.query(BatteryData)
        .filter(BatteryData.timestamp >= since)
        .order_by(BatteryData.timestamp)
        .all()
    )

    if not data:
        return []

    return [
        {
            "timestamp": d.timestamp.isoformat(),
            "voltage": round(d.voltage, 2),
            "current": round(d.current, 2),
            "sharing_power": round(d.voltage * d.current, 2) if d.relay_status == "ON" else 0.0,
            "percentage": d.percentage
        }
        for d in data
    ]