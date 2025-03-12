import datetime as dt
from dataclasses import dataclass
from datetime import timedelta
from jose import jwt, JWTError

from exception import (
    TokenExpired,
    UserNotCorrectPasswordException,
    TokenNotCorrectError,
    UserNotFoundException
)
from models import UserProfile
from repository import UserRepository
from settings import Settings
from schema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException

        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = \
            (dt.datetime.now(dt.timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode(
            claims={
                "user_id": user_id, "expire": expires_date_unix
                },
            key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
            )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> str:
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM]
                )
        except JWTError:
            raise TokenNotCorrectError
        if payload["expire"] < dt.datetime.now(dt.timezone.utc).timestamp():
            raise TokenExpired
        return payload["user_id"]
