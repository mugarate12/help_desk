from fastapi import FastAPI
from app.entities.Session.middlewares.auth_users import auth_users_middleware


def apply_middlewares(app: FastAPI):
    @app.middleware("http")
    async def authentications(request, call_next):
        return await auth_users_middleware(request, call_next)
