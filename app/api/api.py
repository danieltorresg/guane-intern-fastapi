from fastapi import APIRouter

from app.api.endpoints import (
        dog, 
        user, 
        login,
        celery_task,
        )

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(dog.router, prefix="/dogs", tags=["dog"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(celery_task.router, prefix="/task", tags=["celery"])
