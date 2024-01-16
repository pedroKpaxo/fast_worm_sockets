from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.lib.mongo.mongo_client import get_db_handle

from app.routes.chat import chat_router
from app.routes.users import users_router
from app.routes.auth import auth_router
from app.routes.game import game_router

from app.lib.redis.client import get_redis_client
from app.lib.utils.logger import setup_logger

logger = setup_logger('MAIN')

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

# Deal with cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """
    Performs a health check.
    On both the Redis and MongoDB databases.
    """
    redis_client = get_redis_client()
    try:
        redis_client.ping()
        get_db_handle()
        logger.info("Healthy DBS")
        return {"database_status": True}
    except Exception as e:
        logger.error(e)
        return {"database_status": False}


# The routes for the FastAPI app
ROUTES = [
    chat_router,
    users_router,
    auth_router,
    game_router
]

# Include the routes in the FastAPI app
for route in ROUTES:
    app.include_router(route)
