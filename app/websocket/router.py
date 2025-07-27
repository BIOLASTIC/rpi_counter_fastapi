"""Defines the WebSocket endpoint."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive, waiting for client messages if any
            data = await websocket.receive_text()
            # Can add logic here to handle incoming messages from client
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("A client disconnected.")
