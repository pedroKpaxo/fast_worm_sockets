from app.schemas.user import UserBaseSchema, UserResponseSchema


def userEntity(user: UserBaseSchema) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def userResponseEntity(user: UserResponseSchema) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"].isoformat(),
        "updated_at": user["updated_at"].isoformat()
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]
