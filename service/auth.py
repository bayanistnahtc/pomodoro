import datetime as dt
from dataclasses import dataclass
from datetime import timedelta
from jose import jwt, JWTError

from client import GoogleClient, YandexClient
from exception import (
    TokenExpired,
    UserNotCorrectPasswordException,
    TokenNotCorrect,
    UserNotFoundException
)
from models import UserProfile
from repository import UserRepository
from settings import Settings
from schema import UserCreateSchema, UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

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
            raise TokenNotCorrect
        if payload["expire"] < dt.datetime.now(dt.timezone.utc).timestamp():
            raise TokenExpired
        return payload["user_id"]

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(
            email=user_data.email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(
            user_id=created_user.id,
            access_token=access_token
        )

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(
            email=user_data.default_email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )

        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(
            user_id=created_user.id,
            access_token=access_token
        )

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException

        if user.password != password:
            raise UserNotCorrectPasswordException
