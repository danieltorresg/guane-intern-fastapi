from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.param_functions import Body
from starlette.responses import Response

from app.api import deps
from app.api.params.query import QueryPayloadDog
from app.schemas.dog import BaseDog, Dog, UpdateDog
from app.schemas.user import User
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
async def get_all(
    *,
    doggys_in: QueryPayloadDog = Depends(QueryPayloadDog.as_query),
    skip: int = Query(0),
    limit: int = Query(99999),
) -> Optional[List[Dog]]:
    dogs = await dog_service.get_all(
        skip=skip, limit=limit, payload=doggys_in.dict(exclude_none=True)
    )
    if dogs:
        return dogs
    else:
        return []


@router.patch(
    "/adopt/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog adopted"},
        401: {"description": "User unauthorized"},
    },
)
async def adopt(
    *,
    owner_email: str = Body(...),
    name: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Optional[Dog]:
    dog = await dog_service.adopt(
        owner_email=owner_email, name=name, current_user=current_user
    )
    if dog:
        return dog
    raise HTTPException(status_code=404, detail="Dog adopted not found")


@router.get(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog found"},
        401: {"description": "User unauthorized"},
    },
)
async def get_by_name(*, name: str) -> Optional[Dog]:
    dog = await dog_service.get_one_by_name(name=name)
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
    current_user: User = Depends(deps.get_current_active_user),
) -> Optional[Dog]:
    print(dog_in)
    dog = await dog_service.create_by_name(
        dog=dog_in, name=name, in_charge=current_user
    )
    if dog:
        return dog
    return None


@router.patch(
    "/{name}",
    response_model=Union[Dog, None],
    status_code=200,
    responses={
        200: {"description": "Dog updated"},
        401: {"description": "User unauthorized"},
    },
)
async def update_by_name(
    *,
    dog_in: UpdateDog,
    name: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Optional[Dog]:
    dog = await dog_service.update_by_name(
        updated_dog=dog_in, name=name, current_user=current_user
    )
    if dog:
        return dog
    return None


@router.delete(
    "/{name}",
    response_class=Response,
    status_code=200,
    responses={
        200: {"description": "Dog updated"},
        401: {"description": "User unauthorized"},
    },
)
async def delete_by_name(
    *, name: str, current_user: User = Depends(deps.get_current_active_user)
):
    await dog_service.delete(name=name, current_user=current_user)
    dog_deleted_response = Response(status_code=204)
    print(dog_deleted_response)
    return Response(status_code=204)
