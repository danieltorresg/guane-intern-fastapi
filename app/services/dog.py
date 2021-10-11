from typing import List, Optional, Union

from fastapi import HTTPException

from app.config import Settings, get_settings
from app.infra.httpx.client import HTTPClient, client
from app.infra.services.responses import Responses, responses
from app.schemas.dog import AdoptDog, BaseDog, CreateDog, Dog, UpdateDog
from app.schemas.user import User
from app.services.picture import PictureService, picture
from app.services.user import user_service

settings: Settings = get_settings()


class DogService:
    def __init__(self):
        self.__picture: PictureService = picture
        self.__client: HTTPClient = client
        self.__check_codes: Responses = responses
        self.__database_url: str = f"{settings.DATABASE_SERVICE_URL}/api"

    async def get_all(self) -> Optional[List[Dog]]:
        database_url = f"{self.__database_url}/dogs"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return response

    async def create_by_name(
        self, *, dog: BaseDog, name: str, in_charge: User
    ) -> Union[Dog, None]:
        # picture_url = "hola"
        picture_url = await self.__picture.take_picture()
        dog_in = CreateDog(
            id=dog.id,
            name=name,
            picture=picture_url,
        )
        if dog.owner_email:
            owner = await user_service.get_one_by_email(email=dog.owner_email)
            if not owner:
                raise HTTPException(
                    status_code=404,
                    detail="Owner not found: There is not a user with this email",
                )
            else:
                dog_in.owner_id = owner["id"]
                dog_in.in_charge_id = owner["id"]
        else:
            dog_in.in_charge_id = in_charge["id"]
        database_url = f"{self.__database_url}/dogs/{name}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.post(
            url_service=database_url,
            headers=header,
            body=dog_in.dict(exclude_unset=True),
            timeout=40,
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return Dog(**response)

    async def get_one_by_name(self, *, name: str):
        database_url = f"{self.__database_url}/dogs/{name}"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url,
            headers=header,
            timeout=40,
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        return Dog(**response)

    async def get_is_adopted(self, **content) -> Union[dict, None]:
        database_url = f"{self.__database_url}/dogs/is_adopted"
        header = {"Content-Type": "application/json"}
        response = await self.__client.get(
            url_service=database_url, headers=header, timeout=40
        )
        await self.__check_codes.check_codes(response=response)
        response = response.json()
        if response:
            return response
        return None

    async def update_by_name(
        self, *, updated_dog: UpdateDog, name: str, current_user: User
    ) -> Union[dict, None]:
        dog_in_db = (await self.get_one_by_name(name=name)).dict()
        print(updated_dog.picture)
        if dog_in_db:
            if (
                current_user["id"] == dog_in_db["in_charge_id"]
                or current_user["id"] == dog_in_db["owner_id"]
            ):
                if updated_dog.picture:
                    picture_url = await self.__picture.take_picture()
                    updated_dog.picture = picture_url
                database_url = f"{self.__database_url}/dogs/{name}"
                header = {"Content-Type": "application/json"}
                response = await self.__client.patch(
                    url_service=database_url,
                    headers=header,
                    body=updated_dog.dict(exclude_unset=True),
                    timeout=40,
                )
                await self.__check_codes.check_codes(response=response)
                response = response.json()
                return Dog(**response)
            else:
                raise HTTPException(status_code=401, detail="User unauthorized")
        else:
            raise HTTPException(
                status_code=404,
                detail="Dog not found: There is not a dog with this name",
            )

    async def adopt(self, *, owner_email: str, name: str, current_user: User):
        owner = await user_service.get_one_by_email(email=owner_email)
        if owner:
            dog_info = AdoptDog(
                owner_id=owner["id"], is_adopted=True, in_charge_id=owner["id"]
            )
            database_url = f"{self.__database_url}/dogs/adopt/{name}"
            header = {"Content-Type": "application/json"}
            response = await self.__client.patch(
                url_service=database_url,
                headers=header,
                body=dog_info.dict(exclude_unset=True),
                timeout=40,
            )
            await self.__check_codes.check_codes(response=response)
            response = response.json()
            return Dog(**response)
        else:
            raise HTTPException(
                status_code=404,
                detail="Owner not found: There is not a user with this email",
            )

    async def delete(self, *, name: str, current_user: User) -> Union[dict, None]:
        dog_deleted = (await self.get_one_by_name(name=name)).dict()

        if dog_deleted:
            if (
                dog_deleted["owner_id"] == current_user["id"]
                or dog_deleted["in_charge_id"] == current_user["id"]
            ):
                database_url = f"{self.__database_url}/dogs/{name}"
                header = {"Content-Type": "application/json"}
                response = await self.__client.delete(
                    url_service=database_url,
                    headers=header,
                    timeout=40,
                )
                return response
            else:
                raise HTTPException(
                    status_code=401,
                    detail="This user is unauthorized to delete this dog",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Dog not found: There is not a dog with this name",
            )


dog_service = DogService()
