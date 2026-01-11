# schemas.py
from pydantic import BaseModel

class BatteryDataCreate(BaseModel):
    voltage: float
    percentage: int
    current: float

class BatteryDataResponse(BaseModel):
    voltage: float
    percentage: int
    current: float
    relay: str