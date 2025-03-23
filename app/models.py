from sqlalchemy import Column, Integer, String
from .database import Base


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, unique=True, index=True)
    encrypted_password = Column(String)
