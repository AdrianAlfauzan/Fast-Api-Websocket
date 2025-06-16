import uuid
from typing import Dict, List, Tuple
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Key: (channel_type, channel_id), e.g. ('conversation', uuid) or ('chat_room', uuid)
        self.active_connections: Dict[Tuple[str,
                                            uuid.UUID], List[WebSocket]] = {}

    async def connect(self, channel_type: str, channel_id: uuid.UUID, websocket: WebSocket):
        """
        channel_type: 'conversation' or 'chat_room'
        channel_id: UUID of the conversation or chat room
        """
        await websocket.accept()
        key = (channel_type, channel_id)
        self.active_connections.setdefault(key, []).append(websocket)

    def disconnect(self, channel_type: str, channel_id: uuid.UUID, websocket: WebSocket):
        key = (channel_type, channel_id)
        if key in self.active_connections:
            self.active_connections[key].remove(websocket)
            if not self.active_connections[key]:
                del self.active_connections[key]

    async def broadcast(self, channel_type: str, channel_id: uuid.UUID, message: dict):
        key = (channel_type, channel_id)
        for connection in self.active_connections.get(key, []):
            await connection.send_json(message)

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[uuid.UUID, List[WebSocket]] = {}

#     async def connect(self, conversation_id: uuid.UUID, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.setdefault(conversation_id, []).append(websocket)

#     def disconnect(self, conversation_id: uuid.UUID, websocket: WebSocket):
#         self.active_connections[conversation_id].remove(websocket)

#     async def broadcast(self, conversation_id: uuid.UUID, message: dict):
#         for connection in self.active_connections.get(conversation_id, []):
#             await connection.send_json(message)