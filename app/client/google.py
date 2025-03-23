from dataclasses import dataclass

import httpx

from app.settings import Settings
from app.schema import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_access_token(code=code)
        user_info = await self.async_client.get(
                url=self.settings.GOOGLE_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
        print(f"user_info: {user_info.json()}")
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = await self.async_client.post(
                url=self.settings.GOOGLE_TOKEN_URL,
                data=data
            )
        return response.json()["access_token"]
