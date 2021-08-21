from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException

from app.schemas.dog import BaseDog, UpdateDog, Dog
from app.services.dog import dog_service

router = APIRouter()

@router.get(
    "",
    response_model=Union[List[Dog], None],
    status_code=200,
    responses={
        200: {"description": "Dogs found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_all() -> Optional [List[Dog]]:
    dogs = await dog_service.get_all()
    if dogs:
        return dogs
    raise HTTPException(status_code=404, detail="Dogs not found")

    
@router.get(
    "/is_adopted",
    response_model=Union[List[Dog], None],
    status_code=200,
    responses={
        200: {"description": "Dogs founds"},
        401: {"description": "User unauthorized"},
    },
)
async def get_is_adopted() ->  Optional [List[Dog]]:
    dog = await dog_service.get_by_element(is_adopted = True)
    if dog:
        return dog
    raise HTTPException(status_code=404, detail="Dogs adopted not found")


@router.get(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_by_name(*, name: str) -> Optional [Dog]:
    dog = await dog_service.get_one_by_element(name = name)
    if dog:
        return dog
    raise HTTPException(status_code=404, detail="Dog not found")


@router.post(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog created"},
        401: {"description": "User unauthorized"},
    },
)
async def create_by_name(
        *,
        dog_in: BaseDog,
        name: str,
    ) -> Optional [Dog]:
    dog = await dog_service.create_by_name(dog=dog_in, name=name)
    if dog:
        return dog
    return None


@router.put(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog updated"},
        401: {"description": "User unauthorized"},
    },
)
async def update_by_name(*, dog_in: UpdateDog, name: str) -> Optional [Dog]:
    dog = await dog_service.update_by_name(updated_dog= dog_in, name=name)
    if dog:
        return dog
    return None

@router.delete(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog updated"},
        401: {"description": "User unauthorized"},
    },
)
async def delete_by_name(*, name: str) -> Optional [Dog]:
    dog = await dog_service.delete(name=name)
    if dog:
        return dog
    return None

