from typing import Union
from fastapi import HTTPException

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.dog import Dog
from app.schemas.dog import AdoptDog, UpdateDog, CreateDog
from app.schemas.user import User
from app.services.user import user_service


class CRUDDog(CRUDBase[Dog, CreateDog, UpdateDog]):
    async def create(self, *, obj_in: CreateDog) -> Union[dict, None]:
        dog_data = obj_in.dict()
        if await self.get_by_element(name=dog_data["name"]):
            raise HTTPException(status_code=409, detail="Duplicate key: There is a dog with the same name")
        if (type(dog_data["owner_id"]) == int):
            if not await user_service.get_one_by_id(id=dog_data["owner_id"]):
                raise HTTPException(status_code=409, detail="User not found: Invalid user id")            
            dog_data["is_adopted"] = True
        else:
            dog_data["is_adopted"] = False
        dog = await self.model.create(**dog_data)
        return dog

    
    async def delete(self, *, name: str, current_user: User) -> Union[dict, None]:
        dog_deleted = await self.get_by_element(name=name)
        if dog_deleted:
            if dog_deleted[0]["owner_id"]==current_user["id"] or dog_deleted[0]["in_charge_id"]==current_user["id"]:
                model = await self.model.filter(name=name).first().delete()
            else:
                raise HTTPException(status_code=401, detail="This user is unauthorized to deled this dog")
            return dog_deleted[0]
        else:            
            raise HTTPException(status_code=404, detail="Dog not found: There is not a dog with this name")
            

    async def update(
            self, 
            *, 
            name: str, 
            obj_in: Union[UpdateDog, AdoptDog],
            current_user: User,
        ) -> Union[dict, None]:
        dog_in_db = await self.get_by_element(name=name)
        if dog_in_db:
            if current_user["id"] == dog_in_db[0]["owner_id"] or current_user["id"] == dog_in_db[0]["in_charge_id"]:
                dog_updated = await self.model.filter(name=name).update(**obj_in.dict(exclude_unset=True))
                dog_updated = await self.get_by_element(id=dog_in_db[0]["id"])
                return dog_updated[0]
            else:
                raise HTTPException(status_code=401, detail="User unauthorized")
        else:
            raise HTTPException(status_code=404, detail="Dog not found: There is not a dog with this name")
            

dog = CRUDDog(Dog)
