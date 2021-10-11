from jose import jwt
from passlib.context import CryptContext

from app.config import Settings, get_settings

settings: Settings = get_settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityService:    
    def create_access_token(self, id: int, email: str) -> str:
        payload = {"email": email, "id": id}
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

security: SecurityService = SecurityService()
