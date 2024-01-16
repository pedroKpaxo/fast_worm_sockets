from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from starlette import status
from app.lib.mongo.mongo_client import get_db_handle
from app.serializers.user import userEntity, userListEntity

users_router = APIRouter()
templates = Jinja2Templates(directory="templates")


db = get_db_handle()
users_db = db["users"]
USERS_COLLECTION = users_db["users"]


@users_router.get("/users")
async def users(request: Request, response_class=HTMLResponse):
    """Returns all Users in the database."""
    users = await USERS_COLLECTION.find()
    serializbles = userListEntity(users)
    return JSONResponse(content=serializbles)


@users_router.post("/users")
async def create_user(request: Request, response_class=HTMLResponse):
    """Creates a new User in the database."""
    body = await request.json()
    user = await USERS_COLLECTION.insert_one(body)
    serializbles = userEntity(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED,  content=serializbles)  # noqa


@users_router.get("/users/{user_id}")
async def get_user(user_id: str, request: Request, response_class=HTMLResponse):  # noqa
    """Returns a User from the database."""
    user = await USERS_COLLECTION.find_one({"_id": user_id})
    serializbles = userEntity(user)
    return JSONResponse(content=serializbles)
