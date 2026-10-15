from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.get("/")
def health():
    return {"service": "echo", "status": "ok", "websocket": "/ws"}


@app.websocket("/ws")
async def echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            # Echo: reply only to the client that sent the message
            await websocket.send_text(f"Echo: {message}")
    except WebSocketDisconnect:
        pass
