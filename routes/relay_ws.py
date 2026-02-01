# routes/relay_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

clients: list[WebSocket] = []

@router.websocket("/ws/relay")
async def relay_ws(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients.remove(websocket)