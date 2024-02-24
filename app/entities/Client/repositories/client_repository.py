from typing import Optional

from app.core.database.models.clients import ClientsModel
from app.entities.Client.dto.client_dto import ClientDTO
from app.entities.Client.types.repositories.client_repository_types import (
    IClientRepository,
    UserCreatePayload
)


class ClientRepository(IClientRepository):
    def create(self, payload: UserCreatePayload) -> ClientDTO:
        user = self.user_repository.create(payload)

        client = ClientsModel(
            user_id_FK=user.id
        )

        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)

        return ClientDTO(client)

    def get_by_username(self, username: str = '') -> ClientDTO | None:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None

        client = self.session.query(ClientsModel).filter(
            ClientsModel.user_id_FK == user.id).first()
        if not client:
            return None

        self.session.commit()
        self.session.refresh(client)

        return ClientDTO(client)

    def get_by_user_id(self, user_id: str) -> ClientDTO | None:
        client = self.session.query(ClientsModel).filter(
            ClientsModel.user_id_FK == user_id).first()

        if not client:
            return None
        
        self.session.commit()
        self.session.refresh(client)

        return ClientDTO(client)

    def index(self, cursor: str = '', limit: int = 10) -> Optional[dict]:
        clients = self.session.query(ClientsModel)

        if cursor:
            clients = clients.filter(ClientsModel.id > cursor)

        clients = clients.limit(limit).all()

        if not clients:
            return []

        return [ClientDTO(client) for client in clients]
    
    def delete_by_user_id(self, user_id: str) -> Optional[dict]:
        client = self.session.query(ClientsModel).filter(
            ClientsModel.user_id_FK == user_id).first()

        if not client:
            return None
    
        self.session.delete(client)
        self.session.commit()

        user = self.user_repository.get_by_id(user_id)
        self.user_repository.delete_by_id(user.id)

        return client
