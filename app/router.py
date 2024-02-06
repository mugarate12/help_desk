from fastapi import APIRouter

from app.entities.Session.controllers.session_controller import router as session_router

router = APIRouter()


@router.get('/')
async def read_root():
    return {'message': 'Hello World'}

router.include_router(session_router, tags=["session"])
