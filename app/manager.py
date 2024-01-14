from fastapi import WebSocket


class ConnectionManager:
    """
    A base class for managing websocket connections.
    It is used to keep track of active connections and
      broadcast messages to all connected clients.
    """

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        del self.active_connections[self.active_connections.index(websocket)]
