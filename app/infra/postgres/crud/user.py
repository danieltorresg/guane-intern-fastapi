from typing import Any, Dict, Union
from fastapi import HTTPException

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.user import User
from app.schemas.user import BaseUser, UpdateUser, CreateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def create(self, *, obj_in: CreateUser) -> Union[dict, None]:
        user_data = obj_in.dict()
        if await self.get_by_element(email=user_data["email"]):
            raise HTTPException(status_code=409, detail="Duplicate key: There is a user with the same email")
        user = await self.model.create(**user_data)
        return user

    async def delete(self, *, id: str) -> Union[dict, None]:
        user_deleted = await self.get_by_element(id=id)
        if user_deleted:
            model = await self.model.filter(id=id).first().delete()
            return user_deleted[0]
        else:
            raise HTTPException(status_code=404, detail="User not found: There is not a user with this id")

    
    async def update(self, *, id: int, obj_in: UpdateUser) -> Union[dict, None]:
        user_in_db = await self.get_by_element(id=id)
        if user_in_db:
            user_updated = await self.model.filter(id=id).update(**obj_in.dict(exclude_unset=True))
            user_updated = await self.get_by_element(id=id)
            return user_updated[0]
        else:
            raise HTTPException(status_code=404, detail="User not found: There is not a user with this id")


user = CRUDUser(User)