from fastapi import APIRouter, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect


socket_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@socket_router.get("/push")
async def chat(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("chat.html", {"request": request})


@socket_router.websocket("/ws/push")
async def websocket_endpoint(websocket: WebSocket):
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
