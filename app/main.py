from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config.settings import settings
from app.router import router
from app.core.database.init_database import init as init_database
from app.middlewares import apply_middlewares


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

    apply_middlewares(app)
    app.include_router(router)
    init_database()

    return app


app = start_application()
