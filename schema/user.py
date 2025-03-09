from pydantic import BaseModel, Field, model_validator


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: str
    password: str
