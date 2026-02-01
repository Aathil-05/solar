# routes/relay_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

clients: list[WebSocket] = []

@router.websocket("/ws/relay")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    # 🔁 Send current relay state immediately
    await ws.send_text(json.dumps({"relay": relay_status}))

    try:
        while True:
            await ws.receive_text()
    except:
        clients.remove(ws)