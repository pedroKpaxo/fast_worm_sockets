from fastapi import Depends, FastAPI, Request
from typing import Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from motor.core import Database, Collection
from pymongo import MongoClient

from app.lib.mongo.mongo_client import get_db_handle
from app.settings import SETTINGS
from app.serializers.user import userResponseEntity
from app.schemas.user import (
    CreateUserSchema, LoginUserSchema,  UserResponse, UserBaseSchema)
from app.lib.utils.password import hash_password, check_password
from fastapi.security import OAuth2PasswordBearer
import jwt

auth_router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = SETTINGS.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = SETTINGS.REFRESH_TOKEN_EXPIRES_IN

client: MongoClient = get_db_handle()
db: Database = client.get_database('users')
USER_COLLECTION: Collection = db.get_collection('users')


# Instance of OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict) -> str:  # noqa
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=SETTINGS.ACCESS_TOKEN_EXPIRES_IN)  # noqa
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.JWT_PRIVATE_KEY, algorithm=SETTINGS.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    This function takes jwt token, decodes it and return the user data
    """
    try:
        decoded = jwt.decode(token, SETTINGS.JWT_PRIVATE_KEY, algorithms=[SETTINGS.JWT_ALGORITHM])  # noqa
        return decoded
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)  # noqa
async def create_user(payload: CreateUserSchema):
    """
    Basic user registration.
    First, check if the user already exists. And raise an error if it does.
    Then, check if the password and passwordConfirm match. If they
    don't, raise an error.

    If everything is fine, hash the password and
    insert the user into the database.
    """
    # Check if user already exist
    user = await USER_COLLECTION.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exist')  # noqa

    # Compare password and passwordConfirm
    if payload.password != payload.password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')  # noqa

    #  Hash the password
    payload.password = hash_password(payload.password)
    del payload.password_confirm
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    # Insert the user into the database
    result = await USER_COLLECTION.insert_one(payload.model_dump())
    new_user = userResponseEntity(await USER_COLLECTION.find_one({'_id': result.inserted_id}))  # noqa
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_user)


@auth_router.post("/login")
async def login(form_data: LoginUserSchema):
    user = UserBaseSchema(**await USER_COLLECTION.find_one({'email': form_data.email.lower()}))  # noqa
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not check_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"}, headers={"Authorization": f"Bearer {access_token}"})  # noqa


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    verified = verify_token(token)
    user = await USER_COLLECTION.find_one({'email': verified['sub']})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@auth_router.get("/auth/me")
async def read_users_me(current_user: dict = Depends(get_current_user), request: Request = None):  # noqa
    return userResponseEntity(current_user)
