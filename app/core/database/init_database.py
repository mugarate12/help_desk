from app.core.database.base import Base
from app.core.database.session import engine, get_db
from app.core.config.settings import settings
from app.entities.Admin.repositories.admin_repository import AdminsRepository, UserCreatePayload
from app.entities.User.repositories.user_repository import UserRepository
from app.shared.hash import Hash

def _create_initial_admin():
    session = next(get_db())
    user_repository = UserRepository(session)
    admin_repository = AdminsRepository(session, user_repository)

    admin = admin_repository.get_by_username(settings.INITIAL_ADMIN_USERNAME)

    if admin:
        print(f"Admin {settings.INITIAL_ADMIN_USERNAME} already exists")
        return
    else:
        print(f"Creating admin {settings.INITIAL_ADMIN_USERNAME}")

    hash = Hash()

    payload = UserCreatePayload(
        first_name="Admin",
        last_name="Admin",
        username=settings.INITIAL_ADMIN_USERNAME,
        email=settings.INITIAL_ADMIN_EMAIL,
        password=hash.hash_password(settings.INITIAL_ADMIN_PASSWORD),
        address="123 Main St",
        city="Anytown",
        state="CA",
        zip="12345",
        country="USA",
        phone="123-456-7890"
    )

    admin = admin_repository.create(payload)


def init():
    print(f"\033[94m Setup database... \033[0m")
    print(f'Using database: {settings.MYSQL_DB_NAME}')
    print(f'Using host: {settings.MYSQL_HOST}')
    print(f'Using port: {settings.MYSQL_PORT}')
    print(f'Using user: {settings.MYSQL_USER}')
    print(f'Using password: {settings.MYSQL_PWD}')
    print(f'Using url: {settings.DATABASE_URL}')
    print(f"\033[94m Setup database... \033[0m")

    Base.metadata.create_all(bind=engine)
    _create_initial_admin()
