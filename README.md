# CS3720 Activity08 – WebSockets Echo and Chat (FastAPI on Render)

- `echo/` – Echo server. `wss://<host>/ws` sends each message back to the sender only.
- `chat/` – Chat server. `wss://<host>/ws/{username}` broadcasts each message to all connected clients.

Both are deployed as Render web services via `render.yaml` (Blueprint).

Run locally: `pip install -r echo/requirements.txt` then `uvicorn main:app --reload` inside `echo/` or `chat/`.
