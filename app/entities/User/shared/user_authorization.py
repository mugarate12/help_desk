from app.entities.User.types.user_authorization_types import IUserAuthorization
from app.core.users.users_permissions import USERS_TYPES


class UserAuthorization(IUserAuthorization):
    def verify_user_and_get_token(self, username: str, password: str) -> str:
        user = self.users_repository.get_by_username(username)
        print('user: ', user)

        if not user:
            raise Exception('User not found')

        if not self.hash.verify_password(password, user.password):
            raise Exception('Invalid password')

        # verify role of user with repositories of this with id
        role = ''

        admin = self.admin_repository.get_by_user_id(user.id)
        if admin:
            role = USERS_TYPES['ADMIN']

        if role == '':
            raise Exception('User not found')

        token = self.jwt.create({"user_id": user.id, "role": role})
        return token
