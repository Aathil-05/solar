# routes/relay.py
from fastapi import APIRouter

router = APIRouter(prefix="/relay", tags=["relay"])

# Global relay status (consider moving to DB/Redis later)
relay_status = "OFF"

def get_relay_status() -> str:
    return relay_status

@router.get("/status")
def relay_status_api():
    return {"status": relay_status}

@router.get("/on")
def switch_on():
    global relay_status
    relay_status = "ON"
    return {"status": "Relay ON"}

@router.get("/off")
def switch_off():
    global relay_status
    relay_status = "OFF"
    return {"status": "Relay OFF"}