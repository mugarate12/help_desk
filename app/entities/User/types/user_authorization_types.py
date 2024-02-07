from abc import ABC, abstractmethod

from app.core.users.users_permissions import USERS_PERMISSIONS
from app.shared.types.jwt_types import IJWT
from app.shared.types.hash_types import IHash
from app.entities.User.types.user_repository_types import IUserRepository
from app.entities.Admin.types.repositories.admin_repositories_types import IAdminRepository


class IUserAuthorization(ABC):
    jwt: IJWT
    users_permissions: dict[str, dict[str, str]]
    hash = IHash
    users_repository: IUserRepository
    admin_repository: IAdminRepository

    def __init__(self, jwt: IJWT, hash: IHash, users_repository: IUserRepository, admin_repository: IAdminRepository):
        self.jwt = jwt
        self.users_permissions = USERS_PERMISSIONS
        self.hash = hash
        self.users_repository = users_repository
        self.admin_repository = admin_repository

    @abstractmethod
    def verify_user_and_get_token(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def check_authorization(self, token: str, user_type: str):
        pass
