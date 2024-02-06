import os
from dotenv import load_dotenv

config_dir = os.path.dirname(__file__)
config_dir = os.path.join(config_dir, os.pardir, os.pardir, os.pardir)

path = os.path.join(config_dir, '.env')
path = os.path.abspath(path)

load_dotenv(path)


class Settings:
    PROJECT_NAME: str = "Help Desk API"
    PROJECT_VERSION: str = "0.0.1"

    MYSQL_USER: str = os.getenv("PROD_MYSQL_DB_USERNAME", "root")
    MYSQL_PWD = os.getenv("PROD_MYSQL_DB_PASSWORD")
    MYSQL_HOST: str = os.getenv("PROD_MYSQL_DB_HOSTNAME", "localhost")
    MYSQL_PORT: str = os.getenv("PROD_MYSQL_DB_PORT", 3306)
    MYSQL_DB_NAME: str = os.getenv("PROD_MYSQL_DB_NAME", "tdd")

    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}"

    INITIAL_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    INITIAL_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    INITIAL_ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@mail.com")

    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS512")
    ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 24))


settings = Settings()
