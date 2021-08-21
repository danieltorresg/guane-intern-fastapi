from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import Settings, get_settings
from app.schemas.token import Token
from app.services.auth import auth_service


settings: Settings = get_settings()
router = APIRouter()


@router.post("/login/token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await auth_service.authenticate_email(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(
            id=user.id, email=user.email
        ),
        "token_type": "bearer",
    }
