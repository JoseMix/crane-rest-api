from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    apps = relationship("App", back_populates="user")


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    services = Column(String, index=True)
    command = Column(String, index=True)
    ports = Column(String, index=True)
    volumes = Column(String, index=True)
    labels = Column(String, index=True)
    scale = Column(Integer, index=True, default=None)
    image = Column(String, index=True)
    network = Column(String, index=True)
    ip = Column(String, index=True)
    port = Column(String, index=True)
    count = Column(Integer, index=True)
    environment = Column(String, index=True)
    status = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)
    deleted_at = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="apps")
