from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.chat import chat_router
from app.routes.users import users_router
from app.routes.auth import auth_router

# The main FastAPI app
# NOTE: We are using the `StaticFiles` class to serve static files
app = FastAPI(
    title="Fast WormsPy",
    description="A Template for FastAPI Projects using MongoDB, and WebSockets",  # noqa
    version="0.1.0",
    contact={
        "name": "Pedro Cavalcanti",
        "url": "https://github.com/pedrokpaxo",
        "email": "pedrograxxa@gmail.com"
    }
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# The routes for the FastAPI app
ROUTES = [
    chat_router,
    users_router,
    auth_router
]

# Include the routes in the FastAPI app
for route in ROUTES:
    app.include_router(route)
