from typing import Any, Dict, Union
from fastapi import HTTPException

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.dog import Dog
from app.schemas.dog import UpdateDog, CreateDog
from app.services.user import user_service


class CRUDDog(CRUDBase[Dog, CreateDog, UpdateDog]):
    async def create(self, *, obj_in: CreateDog) -> Union[dict, None]:
        dog_data = obj_in.dict()
        if await self.get_by_element(name=dog_data["name"]):
            raise HTTPException(status_code=409, detail="Duplicate key: There is a dog with the same name")
        if (dog_data["owner_id"] ):
            if not await user_service.get_one_by_id(id=dog_data["owner_id"]):
                raise HTTPException(status_code=409, detail="User not found: Invalid user id")            
            dog_data["is_adopted"] = True
        else:
            dog_data["is_adopted"] = False
        dog = await self.model.create(**dog_data)
        return dog

    
    async def delete(self, *, name: str) -> Union[dict, None]:
        dog_deleted = await self.get_by_element(name=name)
        if dog_deleted:
            model = await self.model.filter(name=name).first().delete()
            return dog_deleted[0]
        else:            
            raise HTTPException(status_code=404, detail="Dog not found: There is not a dog with this name")
            

    async def update(self, *, name: str, obj_in: UpdateDog) -> Union[dict, None]:
        dog_in_db = await self.get_by_element(name=name)
        if dog_in_db:
            dog_updated = await self.model.filter(name=name).update(**obj_in.dict(exclude_unset=True))
            dog_updated = await self.get_by_element(name=name)
            return dog_updated[0]
        else:
            raise HTTPException(status_code=404, detail="Dog not found: There is not a dog with this name")


dog = CRUDDog(Dog)
