"""Manages all active WebSocket connections."""
import asyncio
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_json(self, data: dict):
        """Broadcasts a JSON message to all connected clients."""
        # Create a list of tasks for sending messages concurrently
        tasks = [conn.send_json(data) for conn in self.active_connections]
        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

manager = ConnectionManager()
