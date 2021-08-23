from typing import List, Optional, TypeVar, Union
from fastapi import HTTPException

from app.infra.postgres.crud.base import CRUDBase
from app.schemas.dog import AdoptDog, BaseDog, Dog, CreateDog, UpdateDog
from app.infra.postgres.crud.dog import dog
from app.utils.picture import generate_picture
from app.schemas.user import User
from app.services.user import user_service


QueryType = TypeVar("QueryType", bound=CRUDBase)

class DogService:
    def __init__(self, dog_query: QueryType):
        self.__dog_query = dog_query

    async def get_all(self) -> Optional[List[Dog]]:
        dogs = await self.__dog_query.get_all()
        return dogs


    async def create_by_name(
            self,
            *, 
            dog: BaseDog, 
            name: str, 
            in_charge: User
        ) -> Union[dict, None]:
        picture_url = generate_picture()
        dog_in = CreateDog(
                id=dog.id, 
                name=name, 
                picture=picture_url,
            )
        if dog.owner_email:
            owner = await user_service.get_one_by_email(email=dog.owner_email)
            if not owner:
                raise HTTPException(status_code=404, detail="Owner not found: There is not a user with this email")
            else:
                dog_in.owner_id = owner["id"]
                dog_in.in_charge_id = owner["id"]
        else:
            dog_in.in_charge_id = in_charge["id"]
        new_dog_id = await self.__dog_query.create(obj_in=dog_in)
        return new_dog_id


    async def get_one_by_element(self, **content) -> Union[dict, None]:
        doggy = await self.__dog_query.get_by_element(**content)
        if doggy:
            return doggy[0]
        return None


    async def get_by_element(self, **content) -> Union[dict, None]:
        doggy = await self.__dog_query.get_by_element(**content)
        if doggy:
            return doggy
        return None

    
    async def update_by_name(
            self, 
            *, 
            updated_dog: UpdateDog, 
            name: str, 
            current_user: User
        ) -> Union[dict, None]:
        if (updated_dog.picture):
            picture_url = generate_picture()
            updated_dog.picture = picture_url
        dog_updated = await self.__dog_query.update(name=name, obj_in=updated_dog, current_user=current_user)
        return dog_updated

    async def adopt(self,
            *,
            owner_email: str,
            name: str,
            current_user: User
        ):
        owner = await user_service.get_one_by_email(email=owner_email)
        if owner:
            dog_info = AdoptDog(owner_id=owner["id"], is_adopted=True, in_charge_id=owner["id"])
            dog_updated = await self.__dog_query.update(name=name, obj_in=dog_info, current_user=current_user)
            return dog_updated
        else:
            raise HTTPException(status_code=404, detail="Owner not found: There is not a user with this email")
            


    async def delete(self, *, name: str) -> Union[dict, None]:
        dog_deleted = await self.__dog_query.delete(name=name)
        return dog_deleted
        

dog_service = DogService(dog_query = dog)
