import uuid
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[uuid.UUID, List[WebSocket]] = {}

    async def connect(self, conversation_id: uuid.UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(conversation_id, []).append(websocket)

    def disconnect(self, conversation_id: uuid.UUID, websocket: WebSocket):
        self.active_connections[conversation_id].remove(websocket)

    async def broadcast(self, conversation_id: uuid.UUID, message: dict):
        for connection in self.active_connections.get(conversation_id, []):
            await connection.send_json(message)