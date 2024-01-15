from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, StringConstraints
from typing_extensions import Annotated


class UserBaseSchema(BaseModel):
    name: str
    email: str
    password: Annotated[str, StringConstraints(min_length=8)]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class CreateUserSchema(UserBaseSchema):
    password_confirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
