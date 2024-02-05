import uuid
import pytz
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base_class import Base


class UsersModel(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, index=True, default=uuid.uuid4())
    first_name = Column(String(255))
    last_name = Column(String(255))

    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))

    address = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(255))
    country = Column(String(255))

    phone = Column(String(255))
    
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.utc).date())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.utc).date())

    admins = relationship("AdminsModel", back_populates="user")
    clients = relationship("ClientsModel", back_populates="user")