from typing import Union, Any, Optional
from datetime import datetime, timedelta
import jwt
from app.core.config.settings import settings
from app.shared.types.jwt_types import IJWT


class JWT(IJWT):
    def create(self, payload: dict):
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode = {"exp": expire, **payload}

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def decode(self, token: str) -> Optional[dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                                 settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
        except Exception:
            return None
