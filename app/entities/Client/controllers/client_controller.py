from fastapi import APIRouter, HTTPException, status

from app.core.database.session import engine, get_db
from app.shared.hash import Hash
from app.entities.Client.types.repositories.client_repository_types import UserCreatePayload
from app.entities.Client.repositories.client_repository import ClientRepository
from app.entities.User.repositories.user_repository import UserRepository

router = APIRouter()


@router.post('/')
async def create_user(payload: UserCreatePayload):
    try:
        session = next(get_db())
        client_repository = ClientRepository(session, UserRepository(session))

        payload.password = Hash().hash_password(payload.password)
        client_repository.create(payload)

        return {"message": "Client created successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
