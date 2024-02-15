from app.entities.User.types.user_authorization_types import IUserAuthorization
from app.core.users.users_permissions import USERS_TYPES


class UserAuthorization(IUserAuthorization):
    def verify_user_and_get_token(self, username: str, password: str) -> str:
        user = self.users_repository.get_by_username(username)

        if not user:
            raise Exception('User not found')

        if not self.hash.verify_password(password, user.password):
            raise Exception('Invalid password')

        # verify role of user with repositories of this with id
        role = ''

        admin = self.admin_repository.get_by_user_id(user.id)
        if admin:
            role = USERS_TYPES['ADMIN']

        client = self.client_repository.get_by_user_id(user.id)
        if client:
            role = USERS_TYPES['CLIENT']

        if role == '':
            raise Exception('User not found')

        token = self.jwt.create({"user_id": user.id, "role": role})
        return token

    def check_authorization(self, token: str, user_type: str):
        if token == '':
            raise Exception('Token not found')

        payload = self.jwt.decode(token)
        if not payload:
            raise Exception('Invalid token')

        user = self.users_repository.get_by_id(payload['user_id'])

        if not user:
            raise Exception('User not found')

        if user_type == payload['role']:
            admin = self.admin_repository.get_by_user_id(user.id)

            if not admin:
                raise Exception('User not found')
        else:
            raise Exception('You have not permission to access this resource')
