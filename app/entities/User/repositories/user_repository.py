from typing import Optional

from app.core.database.models.users import UsersModel
from app.entities.User.types.user_repository_types import IUserRepository, UserCreatePayload


class UserRepository(IUserRepository):
    def create(self, payload: UserCreatePayload):
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

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_username(self, username: str = '') -> Optional[dict]:
        user = self.session.query(UsersModel).filter(
            UsersModel.username == username).first()
        if not user:
            return None

        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_id(self, id: str) -> Optional[dict]:
        user = self.session.query(UsersModel).filter(
            UsersModel.id == id).first()
        if not user:
            return None

        self.session.commit()
        self.session.refresh(user)

        return user
