from dataclasses import dataclass

import requests

from settings import Settings
from schema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData:
        access_token = self._get_access_token(code=code)
        user_info = requests.get(
            url=self.settings.YANDEX_USER_INFO_URL,
            headers={"Authorization": f"OAuth {access_token}"}
        )
        return YandexUserData(**user_info.json(), access_token=access_token)

    def _get_access_token(self, code: str) -> str:
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
        response = requests.post(
            url=self.settings.YANDEX_TOKEN_URL,
            data=data,
            headers=headers
        )
        return response.json()["access_token"]
