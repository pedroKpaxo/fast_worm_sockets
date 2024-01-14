from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.socket import socket_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(socket_router)
