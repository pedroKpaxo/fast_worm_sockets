import os
from motor.motor_asyncio import AsyncIOMotorClient


def get_db_handle() -> AsyncIOMotorClient:
    """
    This function returns a handle to the MongoDB database.
    Make sure to set the environment variables `MONGO_INITDB_ROOT_USERNAME` and
    `MONGO_INITDB_ROOT_PASSWORD` to the username and password of the MongoDB
    database.
    """
    # NOTE make sure to set the environment variables
    user = os.environ.get('MONGO_INITDB_ROOT_USERNAME', '')
    password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', '')
    client = AsyncIOMotorClient(f'mongodb://{user}:{password}@mongodb:27017')
    return client
