from app.core.database.models.clients import ClientsModel


class ClientDTO():
    model = None

    def __init__(self, client: ClientsModel):
        self.model = client

        self.id = client.id
        self.user_id_FK = client.user_id_FK
        self.created_at = client.created_at
        self.updated_at = client.updated_at

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id_FK': self.user_id_FK,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_model(self) -> ClientsModel:
        return self.model
