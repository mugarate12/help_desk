from sqlalchemy.orm import Session
from abc import ABC


class IRepository(ABC):
    session = None

    def __init__(self, database_session: Session):
        self.session = database_session
