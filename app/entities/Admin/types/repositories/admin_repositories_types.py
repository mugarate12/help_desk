from typing import Optional
from pydantic import BaseModel
from abc import abstractmethod

from app.shared.types.repositories_types import IRepository

class AdminCreatePayload(BaseModel):
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


class IAdminRepository(IRepository):
    @abstractmethod
    def create(self, payload: AdminCreatePayload) -> Optional[dict]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[dict]:
        pass
