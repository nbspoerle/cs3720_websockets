import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, payload: dict):
        # Chat: send every message to all connected clients
        text = json.dumps(payload)
        for connection in list(self.connections):
            try:
                await connection.send_text(text)
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()


@app.get("/")
def health():
    return {"service": "chat", "status": "ok", "clients": len(manager.connections), "websocket": "/ws/{username}"}


@app.websocket("/ws/{username}")
async def chat(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast({"type": "system", "text": f"{username} joined the chat"})
    try:
        while True:
            text = await websocket.receive_text()
            await manager.broadcast({"type": "message", "username": username, "text": text})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "system", "text": f"{username} left the chat"})
