from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.lib.mongo.mongo_client import get_db_handle


users_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@users_router.get("/users")
async def users(request: Request, response_class=HTMLResponse):
    """Returns all Users in the database."""
    client = get_db_handle()
    db = client["users"]
    collection = db["users"]
    print(await collection.find_one())
    pass


@users_router.post("/users")
async def create_user(request: Request, response_class=HTMLResponse):
    """Creates a new User in the database."""
    pass


@users_router.get("/users/{user_id}")
async def get_user(request: Request, response_class=HTMLResponse):
    """Returns a User from the database."""
    pass


@users_router.put("/users/{user_id}")
async def update_user(request: Request, response_class=HTMLResponse):
    """Updates a User in the database."""
    pass


@users_router.delete("/users/{user_id}")
async def delete_user(request: Request, response_class=HTMLResponse):
    """Deletes a User from the database."""
    pass
