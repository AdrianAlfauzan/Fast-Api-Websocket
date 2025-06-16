from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from aiortc import RTCPeerConnection, RTCSessionDescription
import asyncio
import json

router = APIRouter()
pcs = set()

@router.post("/rooms/{room_id}/join")
async def join_room(room_id: str, user_id: str, session: AsyncSession = Depends(get_async_session)):
    # Add user to room_participants table
    await session.execute(
        "INSERT INTO room_participants (room_id, user_id) VALUES (:room_id, :user_id) ON CONFLICT DO NOTHING",
        {"room_id": room_id, "user_id": user_id}
    )
    await session.commit()
    return {"status": "joined"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pc = RTCPeerConnection()
    pcs.add(pc)

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg["type"] == "offer":
                offer = RTCSessionDescription(sdp=msg["sdp"], type=msg["type"])
                await pc.setRemoteDescription(offer)
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await websocket.send_text(json.dumps({
                    "type": pc.localDescription.type,
                    "sdp": pc.localDescription.sdp
                }))
            # Handle ICE candidates, etc.
    finally:
        await pc.close()
        pcs.discard(pc)
