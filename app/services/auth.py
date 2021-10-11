from typing import Optional

from app.config import Settings, get_settings
from app.schemas.user import User
from app.services.security import security
from app.services.user import user_service

settings: Settings = get_settings()


class AuthService:
    def __init__(self):
        return

    async def authenticate_email(self, *, email: str, password: str) -> Optional[User]:
        user = await user_service.get_one_by_email(email=email)
        if not user:
            return None
        if not security.verify_password(password, user["password"]):
            return None
        user = User(**user)
        return user


auth_service = AuthService()
