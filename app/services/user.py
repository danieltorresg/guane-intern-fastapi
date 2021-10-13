from typing import List, Dict, Any, Optional, Union

from passlib.hash import bcrypt

from app.config import Settings, get_settings
from app.infra.httpx.client import HTTPClient, client
from app.infra.services.responses import Responses, responses
from app.schemas.user import CreateUser, UpdateUser, User
from app.services.upload_file import upload

# from app.utils.upload import upload_file


settings: Settings = get_settings()


class UserService:
    def __init__(self):
        self.__client: HTTPClient = client
        self.__check_codes: Responses = responses
        self.__database_url: str = f"{settings.DATABASE_SERVICE_URL}/api"

    async def get_all(
        self,
        payload: Optional[Dict[str, Any]],
        skip: int = 0,
        limit: int = 99999,
        route: Optional[str] = "",
    ) -> Optional[List[User]]:
        if payload:
            payload.update({"skip": skip, "limit": limit})
        else:
            payload = {"skip": skip, "limit": limit}
        database_url = f"{self.__database_url}/users"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url, headers=header, timeout=40, params=payload,
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return response

    async def create(self, new_user: CreateUser) -> Optional[User]:
        new_user.password = bcrypt.hash(new_user.password)
        database_url = f"{self.__database_url}/users"
        header = {"Content-Type": "application/json"}
        user = new_user.dict()
        response = await self.__client.post(
            url_service=database_url, body=user, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return User(**response)

    async def get_one_by_id(self, *, id: int) -> Union[dict, None]:
        database_url = f"{self.__database_url}/users/{id}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        if response:
            return response
        return None

    async def update(self, *, id: int, updated_user: UpdateUser) -> Union[dict, None]:
        if updated_user.password:
            updated_user.password = bcrypt.hash(updated_user.password)
        database_url = f"{self.__database_url}/users/{id}"
        header = {"Content-Type": "application/json"}
        print(updated_user.dict(exclude_unset=True))
        response = await self.__client.patch(
            url_service=database_url,
            headers=header,
            body=updated_user.dict(exclude_unset=True),
            timeout=40,
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return User(**response)

    async def deactivate(self, *, id: int) -> Union[dict, None]:
        updated_user = UpdateUser(is_active=False)
        database_url = f"{self.__database_url}/users/{id}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.patch(
            url_service=database_url,
            headers=header,
            body=updated_user.dict(exclude_unset=True),
            timeout=40,
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return User(**response)

    async def delete(self, *, id: int) -> Union[None]:
        database_url = f"{self.__database_url}/users/{id}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.delete(
            url_service=database_url, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)

    async def upload_file(self) -> dict:
        response = await upload.upload_file()
        return response

    async def get_one_by_email(self, *, email: str) -> Union[dict, None]:
        database_url = f"{self.__database_url}/users/get_by_email/{email}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        if response:
            return response
        return None

    async def get_filter_by_name(self, *, name: str) -> Union[dict, None]:
        database_url = f"{self.__database_url}/users/filter_by_name"
        header = {"Content-Type": "application/json"}
        params = {"name": name}
        response = await self.__client.get(
            url_service=database_url, headers=header, params=params, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return response


user_service = UserService()
