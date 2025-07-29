"""
Defines the WebSocket endpoint.
REVISED: The entire connection lifecycle is now wrapped in a single
try/finally block. This is a more robust pattern that guarantees
the disconnect logic is always called, even if an error occurs
immediately after connection. This resolves the handshake error.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # The fix is to handle the connection and disconnection in a try/finally block.
    await manager.connect(websocket)
    try:
        # This loop keeps the connection open.
        # It waits for the client to send a message (which we don't use)
        # or for the connection to be closed by the client or server.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # This block is executed when the client's browser closes the connection.
        print("A client disconnected cleanly.")
    except Exception as e:
        # This can catch other unexpected errors.
        print(f"An unexpected error occurred in the websocket connection: {e}")
    finally:
        # This block is GUARANTEED to run, whether the disconnect was
        # clean or caused by an error. This prevents stale connections.
        manager.disconnect(websocket)
        print("Connection resources cleaned up.")