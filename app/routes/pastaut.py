from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from motor.core import Database, Collection
from pymongo import MongoClient

from app.lib.mongo.mongo_client import get_db_handle
from app.settings import SETTINGS
from app.serializers.user import userEntity, userResponseEntity
from app.schemas.user import CreateUserSchema, UserResponse
from app.lib.utils.password import hash_password

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = SETTINGS.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = SETTINGS.REFRESH_TOKEN_EXPIRES_IN

client: MongoClient = get_db_handle()
db: Database = client.get_database('users')
USER_COLLECTION: Collection = db.get_collection('users')


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)  # noqa
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
    user = USER_COLLECTION.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exist')  # noqa

    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')  # noqa

    #  Hash the password
    payload.password = hash_password(payload.password)
    del payload.passwordConfirm
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    # Insert the user into the database
    result = USER_COLLECTION.insert_one(payload.model_dump())
    new_user = userResponseEntity(USER_COLLECTION.find_one({'_id': result.inserted_id}))  # noqa
    return Response(status_code=status.HTTP_201_CREATED, content=new_user)


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    """
    A route for refreshing the access token.
    If the refresh token is valid, create a new access token and return it.
    """
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not refresh access token'
            )

        user = userEntity(USER_COLLECTION.find_one({'_id': ObjectId(str(user_id))}))  # noqa
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='The user belonging to this token no logger exist'
            )

        access_token = Authorize.create_access_token(
            subject=str(user["id"]),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
        )
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')  # noqa
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)  # noqa

    acess_cookie = {
        'key': 'access_token',
        'value': access_token,
        'max_age': ACCESS_TOKEN_EXPIRES_IN * 60,
        'expires': ACCESS_TOKEN_EXPIRES_IN * 60,
    }
    logged_in_cookie = {
        'key': 'logged_in',
        'value': 'True',
        'max_age': ACCESS_TOKEN_EXPIRES_IN * 60,
        'expires': ACCESS_TOKEN_EXPIRES_IN * 60,
    }
    response.set_cookie(**acess_cookie)
    response.set_cookie(**logged_in_cookie)
    return Response(status_code=status.HTTP_200_OK, content={'access_token': access_token})  # noqa


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends()):  # noqa
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return Response(status_code=status.HTTP_200_OK, content={'message': 'Successfully logged out'})  # noqa
