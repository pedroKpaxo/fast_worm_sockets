import base64
import os
from typing import List
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


class OAuthSettings(BaseModel):
    authjwt_algorithm: str = SETTINGS.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [SETTINGS.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(SETTINGS.JWT_PUBLIC_KEY).decode('utf-8')  # noqa
    authjwt_private_key: str = base64.b64decode(SETTINGS.JWT_PRIVATE_KEY).decode('utf-8')  # noqa
