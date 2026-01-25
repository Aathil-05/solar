from fastapi import APIRouter, HTTPException

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

# 🔹 Turn ON a relay
@router.get("/{relay_name}/on")
def switch_on(relay_name: str):
    if relay_name not in relay_status:
        raise HTTPException(status_code=404, detail="Relay not found")

    relay_status[relay_name] = "ON"
    return {"relay": relay_name, "status": "ON"}

# 🔹 Turn OFF a relay
@router.get("/{relay_name}/off")
def switch_off(relay_name: str):
    if relay_name not in relay_status:
        raise HTTPException(status_code=404, detail="Relay not found")

    relay_status[relay_name] = "OFF"
    return {"relay": relay_name, "status": "OFF"}
