from typing import Dict, List, Optional, Union
from fastapi import APIRouter

from app.celery.celery import app


router = APIRouter()

@router.get(
    "",
    response_model=Union[Dict, None],
    status_code=200,
    responses={
        200: {"description": "Excellent"},
        401: {"description": "User unauthorized"},
    },
)
async def complex_task(time: str) -> Optional [Dict]:
    app.send_task("task.complex_task", kwargs={"secs":time})
    return {
        "details":"Excellent"
    }