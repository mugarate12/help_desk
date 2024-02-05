from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config.settings import settings
from app.router import router
from app.core.database.init_database import init


def start_application():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=[
                '*',
                'http://127.0.0.1'
            ],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
    ]

    app = FastAPI(
        title=settings,
        version=settings.PROJECT_VERSION,
        middleware=middleware
    )

    app.include_router(router)
    init()

    return app


app = start_application()
