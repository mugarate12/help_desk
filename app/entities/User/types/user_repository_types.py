from typing import Optional
from abc import abstractmethod
from pydantic import BaseModel
from typing import Optional

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

class UserUpdatePayload(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]

    phone: Optional[str]

class IUserRepository(IRepository):
    @abstractmethod
    def create(self, payload: UserCreatePayload):
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def update_by_id(self, id: str, payload: UserUpdatePayload) -> Optional[dict]:
        pass
