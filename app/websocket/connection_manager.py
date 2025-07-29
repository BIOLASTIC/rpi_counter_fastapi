"""
Manages all active WebSocket connections.
This file is already correct, but provided for completeness.
"""
import asyncio
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts a new websocket connection and adds it to the active list."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a websocket connection from the active list."""
        self.active_connections.remove(websocket)

    async def broadcast_json(self, data: dict):
        """Broadcasts a JSON message to all connected clients concurrently."""
        if not self.active_connections:
            return

        # Create a list of tasks for sending messages
        tasks = [conn.send_json(data) for conn in self.active_connections]
        
        # gather waits for all tasks to complete. return_exceptions=True prevents
        # one failed send from crashing the entire broadcast loop.
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Optional: Log any errors that occurred during broadcast
        for result in results:
            if isinstance(result, Exception):
                print(f"Error broadcasting websocket message: {result}")

# A single, shared instance for the entire application
manager = ConnectionManager()