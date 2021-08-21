from typing import List, Optional, TypeVar, Union

from app.infra.postgres.crud.base import CRUDBase, crud
from app.schemas.user import User, CreateUser, UpdateUser


QueryType = TypeVar("QueryType", bound=CRUDBase)

class UserService:
    def __init__(self, user_query: QueryType):
        self.__user_query = user_query

    async def get_all(self) -> Optional[List[User]]:
        users = await self.__user_query.get_all()
        return users

    
    async def create(self, new_user: CreateUser) -> Optional[User]:
        user = await self.__user_query.create(obj_in=new_user)
        return user

    
    async def get_one_by_id(self, *, id: int) -> Union[dict, None]:
        user = await self.__user_query.get_by_element(id=id)
        if user:
            return user[0]
        return None

    
    async def get_one_by_email(self, *, email: str) -> Union[dict, None]:
        user = await self.__user_query.get_by_element(email=email)
        if user:
            return user[0]
        return None

    
    async def update(self, *, id: int, updated_user: UpdateUser) -> Union[dict, None]:
        dog_updated = await self.__user_query.update(id=id, obj_in=updated_user)
        return dog_updated

    
    async def deactivate(self, *, id: int) -> Union[dict, None]:
        deactivate = UpdateUser(is_active=False)
        dog_updated = await self.__user_query.update(id=id, obj_in=deactivate)
        return dog_updated


    async def delete(self, *, id: int) -> Union[dict, None]:
        user_deleted = await self.__user_query.delete(id=id)
        return user_deleted


user_service = UserService(user_query = crud)
