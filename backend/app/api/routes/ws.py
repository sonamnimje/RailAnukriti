from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set


router = APIRouter()


class ConnectionManager:
	def __init__(self) -> None:
		self.active_connections: Set[WebSocket] = set()

	async def connect(self, websocket: WebSocket) -> None:
		await websocket.accept()
		self.active_connections.add(websocket)

	def disconnect(self, websocket: WebSocket) -> None:
		self.active_connections.discard(websocket)

	async def broadcast(self, message: str) -> None:
		for connection in list(self.active_connections):
			try:
				await connection.send_text(message)
			except Exception:
				self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket) -> None:
	await manager.connect(websocket)
	try:
		while True:
			await websocket.receive_text()
			# Echo for now; in production, push live train updates
			await websocket.send_text("pong")
	except WebSocketDisconnect:
		manager.disconnect(websocket)


