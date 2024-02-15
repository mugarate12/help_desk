from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse

from app.core.database.session import get_db
from app.shared.jwt import JWT
from app.shared.hash import Hash
from app.entities.User.shared.user_authorization import UserAuthorization
from app.entities.Admin.repositories.admin_repository import AdminsRepository
from app.entities.Client.repositories.client_repository import ClientRepository
from app.entities.User.repositories.user_repository import UserRepository
from app.core.users.users_permissions import USERS_TYPES

session = next(get_db())
users_repository = UserRepository(database_session=session)

user_authorization = UserAuthorization(
    jwt=JWT(),
    admin_repository=AdminsRepository(
        database_session=session, user_repository=users_repository),
    client_repository=ClientRepository(
        database_session=session, user_repository=users_repository
    ),
    hash=Hash(),
    users_repository=users_repository
)


async def auth_users_middleware(request: Request, call_next):
    path = request.url.path
    authorization = request.headers.get('Authorization')
    token = ''

    if authorization and 'Bearer' in authorization:
        token = authorization.split('Bearer ')[1]

    try:
        if 'admins' in str(path):
            user_authorization.check_authorization(token, USERS_TYPES['ADMIN'])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"error": str(e)})

    response = await call_next(request)
    return response
