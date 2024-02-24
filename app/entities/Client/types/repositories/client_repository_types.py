from sqlalchemy.orm import Session
from typing import Optional
from abc import abstractmethod

from app.shared.types.repositories_types import IRepository
from app.entities.User.types.user_repository_types import UserCreatePayload, UserUpdatePayload
from app.entities.User.repositories.user_repository import UserRepository
from app.entities.Client.dto.client_dto import ClientDTO

class IClientRepository(IRepository):
    user_repository: UserRepository

    def __init__(self, database_session: Session, user_repository: UserRepository):
        super().__init__(database_session)
        self.user_repository = user_repository

    @abstractmethod
    def create(self, payload: UserCreatePayload) -> ClientDTO:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> ClientDTO:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> ClientDTO | None:
        pass

    @abstractmethod
    def index(self, cursor: str = '', limit: int = 10) -> Optional[dict]:
        pass

    @abstractmethod
    def delete_by_user_id(self, user_id: str) -> Optional[dict]:
        pass
