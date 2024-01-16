from fastapi import APIRouter, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from game.handler import RouletteGameManager

game_router = APIRouter()
templates = Jinja2Templates(directory="templates")

manager = RouletteGameManager()


@game_router.get("/game/")
def get_game(request: Request, response_class=HTMLResponse):
    """ A simple endpoint to render the game page."""
    return templates.TemplateResponse("game.html", {"request": request})


@game_router.websocket("/game/start/ws")
async def websocket_start_game(websocket: WebSocket):
    """
    The main websocket endpoint for the game.
    It will handle the initial connection and dispatch
      it to the correct handler.
    """
    await manager.initial_game_handler(websocket)
