from fastapi import APIRouter

from app.entities.Client.controllers.client_controller import router as client_router
from app.entities.Session.controllers.session_controller import router as session_router

router = APIRouter()


@router.get('/')
async def read_root():
    return {'message': 'Hello World'}

@router.get('/admins')
async def read_root():
    return {'message': 'Hello World'}

router.include_router(client_router, tags=["clients"], prefix="/clients")
router.include_router(session_router, tags=["session"])
