import os
from pydantic import BaseModel


class CoreSettings(BaseModel):

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str


SETTINGS = CoreSettings(
    JWT_ALGORITHM=os.environ.get('JWT_ALGORITHM', 'HS256'),
    JWT_PUBLIC_KEY=os.environ.get('JWT_PUBLIC_KEY', ''),
    JWT_PRIVATE_KEY=os.environ.get('JWT_PRIVATE_KEY', ''),
    REFRESH_TOKEN_EXPIRES_IN=int(os.environ.get('REFRESH_TOKEN_EXPIRES_IN', 30)),  # noqa
    ACCESS_TOKEN_EXPIRES_IN=int(os.environ.get('ACCESS_TOKEN_EXPIRES_IN', 15)),  # noqa

)
