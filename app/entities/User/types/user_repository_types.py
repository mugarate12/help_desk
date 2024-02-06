from typing import Optional
from abc import abstractmethod
from pydantic import BaseModel

from app.shared.types.repositories_types import IRepository

class UserCreatePayload(BaseModel):
    first_name: str
    last_name: str

    username: str
    email: str
    password: str

    address: str
    city: str
    state: str
    zip: str
    country: str

    phone: str

class IUserRepository(IRepository):
    @abstractmethod
    def create(self, payload: UserCreatePayload):
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[dict]:
        pass
