from passlib.context import CryptContext

from app.shared.types.hash_types import IHash

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class Hash(IHash):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)
