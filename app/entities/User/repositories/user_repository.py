from typing import Optional

from app.core.database.models.users import UsersModel
from app.entities.User.types.user_repository_types import IUserRepository, UserCreatePayload, UserUpdatePayload


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
    
    def update_by_id(self, id: str, payload: UserUpdatePayload) -> Optional[dict]:
        user = self.get_by_id(id)
        if not user:
            return None
        
        if payload.first_name:
            user.first_name = payload.first_name
        if payload.last_name:
            user.last_name = payload.last_name
        if payload.username:
            user.username = payload.username
        if payload.email:
            user.email = payload.email
        if payload.password:
            user.password = payload.password
        if payload.address:
            user.address = payload.address
        if payload.city:
            user.city = payload.city
        if payload.state:
            user.state = payload.state
        if payload.zip:
            user.zip = payload.zip
        if payload.country:
            user.country = payload.country
        if payload.phone:
            user.phone = payload.phone

        self.session.commit()
        self.session.refresh(user)

        return user
