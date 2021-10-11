from requests import get

from app.config import Settings, get_settings
from app.infra.httpx.client import client

settings: Settings = get_settings()


class PictureService:    
    async def take_picture(self):
        url = settings.IMAGE_API
        header = {"Content-Type": "application/json"}
        response = await client.get(url_service=url, headers=header, timeout=40)
        response = response.json()["message"]
        return response

picture: PictureService = PictureService()
