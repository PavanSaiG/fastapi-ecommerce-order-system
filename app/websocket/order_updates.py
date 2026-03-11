from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # Store connections by order_id
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, order_id: int):
        await websocket.accept()
        if order_id not in self.active_connections:
            self.active_connections[order_id] = []
        self.active_connections[order_id].append(websocket)

    def disconnect(self, websocket: WebSocket, order_id: int):
        self.active_connections[order_id].remove(websocket)
        if not self.active_connections[order_id]:
            del self.active_connections[order_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_status(self, order_id: int, status: str):
        if order_id in self.active_connections:
            for connection in self.active_connections[order_id]:
                await connection.send_text(f"Order {order_id} status changed to: {status}")

manager = ConnectionManager()
