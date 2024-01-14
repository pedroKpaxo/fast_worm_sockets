from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.socket import socket_router
from app.routes.users import users_router

# The main FastAPI app
# NOTE: We are using the `StaticFiles` class to serve static files
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# The routes for the FastAPI app
ROUTES = [
    socket_router,
    users_router
]

# Include the routes in the FastAPI app
for route in ROUTES:
    app.include_router(route)
