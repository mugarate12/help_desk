from fastapi import APIRouter, HTTPException, status

from app.core.database.session import get_db
from app.shared.jwt import JWT
from app.shared.hash import Hash
from app.entities.User.shared.user_authorization import UserAuthorization
from app.entities.Admin.repositories.admin_repository import AdminsRepository
from app.entities.User.repositories.user_repository import UserRepository
from app.entities.Session.types.session_controller_types import LoginBody

session = next(get_db())
users_repository = UserRepository(database_session=session)

user_authorization = UserAuthorization(
    jwt=JWT(),
    admin_repository=AdminsRepository(
        database_session=session, user_repository=users_repository),
    hash=Hash(),
    users_repository=users_repository
)

router = APIRouter()

@router.post('/login', response_model=dict, status_code=status.HTTP_200_OK)
async def login(body: LoginBody):
    payload = body.dict(exclude_unset=True)

    try:
        token = user_authorization.verify_user_and_get_token(payload['username'], payload['password'])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return {"token": token}