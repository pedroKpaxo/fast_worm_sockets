

from abc import ABC
import asyncio

from fastapi import WebSocket
from game.events.schemas import ErrorEvent

from game.main import Game
from game.player.schema import Player
from typing import TypedDict


class PlayerConnection(TypedDict):
    """A player connection."""

    player: Player
    websocket: WebSocket


class GamePlayMode(Game):
    """A class to represent the game play mode."""

    def __init__(self):
        """Initialize the game play mode."""
        super().__init__()
        self.connections: dict[WebSocket, str] = {}


class BroadcastManager(ABC):
    async def broadcast(self, game: GamePlayMode, message: str):
        """
        Broadcast a message to all connected clients.
        """
        await asyncio.gather(
            *[connection.send_json(message) for connection in game.connections]
        )

    async def send_error(self, websocket: WebSocket, message: str):
        error_event = ErrorEvent(message=message)
        await websocket.send_json(error_event.model_dump())
