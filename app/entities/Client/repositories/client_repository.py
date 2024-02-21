from typing import Optional

from app.core.database.models.clients import ClientsModel
from app.entities.Client.types.repositories.client_repository_types import (
    IClientRepository,
    UserCreatePayload
)


class ClientRepository(IClientRepository):
    def create(self, payload: UserCreatePayload) -> dict:
        user = self.user_repository.create(payload)

        client = ClientsModel(
            user_id_FK=user.id
        )

        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

        return {
            "id": client.id,
            "user_id_FK": client.user_id_FK,
            "created_at": client.created_at,
            "updated_at": client.updated_at
        }

    def get_by_username(self, username: str = '') -> Optional[dict]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None

        client = self.session.query(ClientsModel).filter(
            ClientsModel.user_id_FK == user.id).first()
        if not client:
            return None

        self.session.commit()
        self.session.refresh(client)

        return {
            "id": client.id,
            "user_id_FK": client.user_id_FK,
            "created_at": client.created_at,
            "updated_at": client.updated_at,
            "password": user.password
        }

    def get_by_user_id(self, user_id: str) -> Optional[dict]:
        client = self.session.query(ClientsModel).filter(
            ClientsModel.user_id_FK == user_id).first()

        if not client:
            return None

        self.session.commit()
        self.session.refresh(client)

        return client

    def index(self, cursor: str = '', limit: int = 10) -> Optional[dict]:
        clients = self.session.query(ClientsModel)

        if cursor:
            clients = clients.filter(ClientsModel.id > cursor)

        clients = clients.limit(limit).all()

        if not clients:
            return []

        return clients
