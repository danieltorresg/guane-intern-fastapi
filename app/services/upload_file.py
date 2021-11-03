from app.config import Settings, get_settings
from app.infra.httpx.client import client

settings: Settings = get_settings()


class UploadService:
    async def upload_file(self):
        url = "https://gttb.guane.dev/api/files"
        with open("./app/utils/file.txt", mode="rb") as file:
            fileContent = file.read()
        headers = {
            "accept": "application/json",
            "Content-Type": "multipart/form-data",
        }
        files = {
            "file": fileContent,
        }
        response = await client.post(
            url_service=url, headers=headers, timeout=40, file=files
        )
        response = response.json()["message"]
        return response


upload: UploadService = UploadService()
