from typing import Optional

from app.core.database.models.admins import AdminsModel
from app.core.database.models.users import UsersModel
from app.entities.Admin.types.repositories.admin_repositories_types import (
    IAdminRepository,
    AdminCreatePayload
)


class AdminsRepository(IAdminRepository):
    def create(self, payload: AdminCreatePayload) -> dict:
        print(payload)

        user = UsersModel(
            first_name=payload.first_name,
            last_name=payload.last_name,
            username=payload.username,
            email=payload.email,
            password=payload.password,
            address=payload.address,
            city=payload.city,
            state=payload.state,
            zip=payload.zip,
            country=payload.country,
            phone=payload.phone
        )

        print('cheguei aqui 1')

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        print('cheguei aqui 2')

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
        user = self.session.query(UsersModel).filter(
            UsersModel.username == username).first()
        if not user:
            return None

        self.session.commit()
        self.session.refresh(user)

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
            "updated_at": admin.updated_at
        }
