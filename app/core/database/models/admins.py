import uuid
import pytz
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base_class import Base

class AdminsModel(Base):
    __tablename__ = "admins"

    id = Column(String(255), primary_key=True, index=True, default=uuid.uuid4())
    user_id_FK = Column(String(255), ForeignKey('users.id'))

    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.utc).date())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.utc).date())

    user = relationship("UsersModel", back_populates="admins")
