from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

class AuthService:

    def hash_password(self, password: str) -> str:
        print(">>> PASSWORD RECEIVED BY hash_password():", password)
        print(">>> TYPE:", type(password))
        if isinstance(password, str):
            print(">>> LENGTH:", len(password))
        else:
            print(">>> LENGTH: NOT A STRING")
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


auth_service = AuthService()
