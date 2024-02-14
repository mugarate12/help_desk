from typing import Optional

from app.core.database.models.admins import AdminsModel
from app.entities.Admin.types.repositories.admin_repositories_types import (
    IAdminRepository,
    UserCreatePayload
)


class AdminsRepository(IAdminRepository):
    def create(self, payload: UserCreatePayload) -> dict:
        user = self.user_repository.create(payload)

        admin = AdminsModel(
            user_id_FK=user.id
        )

        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)

        return {
            "id": admin.id,
            "user_id_FK": admin.user_id_FK,
            "created_at": admin.created_at,
            "updated_at": admin.updated_at
        }

    def get_by_username(self, username: str = '') -> Optional[dict]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None

        admin = self.session.query(AdminsModel).filter(
            AdminsModel.user_id_FK == user.id).first()
        if not admin:
            return None

        self.session.commit()
        self.session.refresh(admin)

        return {
            "id": admin.id,
            "user_id_FK": admin.user_id_FK,
            "created_at": admin.created_at,
            "updated_at": admin.updated_at,
            "password": user.password
        }

    def get_by_user_id(self, user_id: str) -> Optional[dict]:
        admin = self.session.query(AdminsModel).filter(
            AdminsModel.user_id_FK == user_id).first()
        
        if not admin:
            return None
        
        self.session.commit()
        self.session.refresh(admin)

        return admin
