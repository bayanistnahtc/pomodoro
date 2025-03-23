from dataclasses import dataclass

import httpx

from app.settings import Settings
from app.schema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_access_token(code=code)

        user_info = await self.async_client.get(
                url=self.settings.YANDEX_USER_INFO_URL,
                headers={"Authorization": f"OAuth {access_token}"}
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            "redirect_uri": self.settings.YANDEX_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = await self.async_client.post(
                url=self.settings.YANDEX_TOKEN_URL,
                data=data,
                headers=headers
            )
        return response.json()["access_token"]
