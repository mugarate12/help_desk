from fastapi import APIRouter, HTTPException, status, Request
from typing import Optional
from pydantic import BaseModel

from app.core.database.session import engine, get_db
from app.shared.hash import Hash
from app.shared.jwt import JWT
from app.entities.Client.types.repositories.client_repository_types import UserCreatePayload, UserUpdatePayload
from app.entities.Admin.repositories.admin_repository import AdminsRepository
from app.entities.Client.repositories.client_repository import ClientRepository
from app.entities.User.repositories.user_repository import UserRepository
from app.entities.User.shared.user_authorization import UserAuthorization

router = APIRouter()


class ClientUpdateBody(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]

    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]

    phone: Optional[str]


class ClientUpdateBodyByClient(ClientUpdateBody):
    old_password: Optional[str]


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


@router.get('/')
async def get_all_clients():
    try:
        session = next(get_db())
        user_repository = UserRepository(session)
        client_repository = ClientRepository(session, user_repository)

        clients = client_repository.index()

        clients_formatted = []
        for client in clients:
            client_dict = client.__dict__.copy()
            user = user_repository.get_by_id(client_dict['user_id_FK'])
            user = user.__dict__.copy()

            del user['password']

            clients_formatted.append({**client_dict, "user": user})

        return {
            'result': clients_formatted
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get('/{user_id}')
async def get_client(user_id: str):
    try:
        session = next(get_db())
        client_repository = ClientRepository(session, UserRepository(session))

        client = client_repository.get_by_user_id(user_id)
        client_dict = client.__dict__.copy()

        user = client_repository.user_repository.get_by_id(
            client_dict['user_id_FK'])
        user_dict = user.__dict__.copy()

        del user_dict['password']

        return {
            'result': {
                **client_dict,
                "user": user_dict
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put('/{user_id}')
async def update_client_by_admin(user_id: str, payload: ClientUpdateBody):
    try:
        session = next(get_db())
        client_repository = ClientRepository(session, UserRepository(session))

        # verify if user exists
        user = client_repository.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        client = client_repository.get_by_user_id(user_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        client_dict = client.__dict__.copy()

        # update user
        update_payload = UserUpdatePayload()

        if payload.first_name:
            update_payload.first_name = payload.first_name
        if payload.last_name:
            update_payload.last_name = payload.last_name
        if payload.username:
            update_payload.username = payload.username
        if payload.email:
            update_payload.email = payload.email
        if payload.address:
            update_payload.address = payload.address
        if payload.city:
            update_payload.city = payload.city
        if payload.state:
            update_payload.state = payload.state
        if payload.zip:
            update_payload.zip = payload.zip
        if payload.country:
            update_payload.country = payload.country
        if payload.phone:
            update_payload.phone = payload.phone

        if payload.password:
            update_payload.password = Hash().hash_password(payload.password)

        user = client_repository.user_repository.update_by_id(
            user.id, update_payload)
        user_dict = user.__dict__.copy()

        return {
            'result': {
                **client_dict,
                "user": user_dict
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put('/')
async def update_client(payload: ClientUpdateBodyByClient, request: Request):
    try:
        session = next(get_db())
        user_repository = UserRepository(session)
        admin_repository = AdminsRepository(session, user_repository)
        client_repository = ClientRepository(session, user_repository)
        hash = Hash()

        user_authorization = UserAuthorization(
            jwt=JWT(),
            hash=hash,
            users_repository=user_repository,
            admin_repository=admin_repository,
            client_repository=client_repository,
        )

        user_data = user_authorization.get_user_data_from_request(request)
        user_id = user_data['id']

        # verify if user exists
        user = client_repository.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        client = client_repository.get_by_user_id(user_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        client_dict = client.__dict__.copy()

        # update user
        update_payload = UserUpdatePayload()

        if payload.first_name:
            update_payload.first_name = payload.first_name
        if payload.last_name:
            update_payload.last_name = payload.last_name
        if payload.username:
            update_payload.username = payload.username
        if payload.email:
            update_payload.email = payload.email
        if payload.address:
            update_payload.address = payload.address
        if payload.city:
            update_payload.city = payload.city
        if payload.state:
            update_payload.state = payload.state
        if payload.zip:
            update_payload.zip = payload.zip
        if payload.country:
            update_payload.country = payload.country
        if payload.phone:
            update_payload.phone = payload.phone

        if payload.password:
            if payload.old_password:
                is_verified = hash.verify_password(
                    payload.old_password, user.password)

                if not is_verified:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

                update_payload.password = hash.hash_password(payload.password)
                pass
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is required to change password")

        user = client_repository.user_repository.update_by_id(
            user.id, update_payload)
        user_dict = user.__dict__.copy()

        return {
            'result': {
                **client_dict,
                "user": user_dict
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.delete('/{user_id}')
async def delete_client_by_admin(user_id: str):
    try:
        session = next(get_db())
        user_repository = UserRepository(session)
        client_repository = ClientRepository(session, user_repository)

        client_repository.delete_by_user_id(user_id)

        return {"message": "Client deleted successfully!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))