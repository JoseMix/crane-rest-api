from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(String, index=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(String, index=True)


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(String, index=True)


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
    hosts = Column(String, index=True)
    ip = Column(String, index=True)
    port = Column(String, index=True)
    count = Column(Integer, index=True)
    environment = Column(String, index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="apps")


class OPAConfig(Base):
    __tablename__ = 'opa_config'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    threshold = Column(Integer, nullable=False)
    policy_status = Column(String, nullable=False)
    policy = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(String, nullable=True)


class OPAStatic(Base):
    __tablename__ = 'opa_static'

    id = Column(Integer, primary_key=True)
    package = Column(String, nullable=False)
    default_status = Column(String, nullable=False)
