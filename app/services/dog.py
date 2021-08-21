from typing import List, Optional, TypeVar, Union

from app.infra.postgres.crud.base import CRUDBase, crud
from app.schemas.dog import BaseDog, Dog, CreateDog, UpdateDog
from app.utils.picture import generate_picture


QueryType = TypeVar("QueryType", bound=CRUDBase)

class DogService:
    def __init__(self, dog_query: QueryType):
        self.__dog_query = dog_query

    async def get_all(self) -> Optional[List[Dog]]:
        dogs = await self.__dog_query.get_all()
        return dogs


    async def create_by_name(self, *, dog: BaseDog, name: str) -> Union[dict, None]:
        picture_url = generate_picture()
        dog_in = CreateDog(id=dog.id, name=name, picture=picture_url, owner_id=dog.owner_id)
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

    
    async def update_by_name(self, *, updated_dog: UpdateDog, name: str) -> Union[dict, None]:
        if (updated_dog.picture):
            picture_url = generate_picture()
            updated_dog.picture = picture_url
        if (updated_dog.owner_id):
            updated_dog.is_adopted = True
        dog_updated = await self.__dog_query.update(name=name, obj_in=updated_dog)
        return dog_updated


    async def delete(self, *, name: str) -> Union[dict, None]:
        dog_deleted = await self.__dog_query.delete(name=name)
        return dog_deleted
        

dog_service = DogService(dog_query = crud)
