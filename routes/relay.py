from fastapi import APIRouter, HTTPException
import json
from routes.relay_ws import clients

router = APIRouter(prefix="/relay", tags=["relay"])

# Multiple relay statuses
relay_status = {
    "home": "OFF",
    "neighbour": "OFF",
    "solar": "OFF"
}

def get_relay_status(relay_name: str) -> str:
    if relay_name not in relay_status:
        raise HTTPException(status_code=404, detail="Relay not found")
    return relay_status[relay_name]



async def broadcast():
    for ws in clients:
        await ws.send_text(json.dumps({
            "relay": relay_status
        }))


# 🔹 Get status of all relays
@router.get("/status")
def all_relay_status():
    return relay_status

# 🔹 Get status of a specific relay
@router.get("/{relay_name}/status")
def relay_status_api(relay_name: str):
    return {
        "relay": relay_name,
        "status": get_relay_status(relay_name)
    }

@router.get("/{relay_name}/on")
async def switch_on(relay_name: str):
    relay_status[relay_name] = "ON"
    await broadcast()
    return {"relay": relay_name, "status": "ON"}

@router.get("/{relay_name}/off")
async def switch_off(relay_name: str):
    relay_status[relay_name] = "OFF"
    await broadcast()
    return {"relay": relay_name, "status": "OFF"}

