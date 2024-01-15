from fastapi import APIRouter, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect


chat_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@chat_router.get("/chat")
async def chat(request: Request, response_class=HTMLResponse):
    """Current just for testing purposes"""
    # TODO add authentication
    # TODO add chat logic
    return templates.TemplateResponse("chat.html", {"request": request})


@chat_router.websocket("/ws/chat")
async def chat_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_text()
                await websocket.send_text(f"Message text was: {data}")
            except WebSocketDisconnect:
                print("Client disconnected")
                break
    except Exception as e:
        print(f"Error: {e}")
