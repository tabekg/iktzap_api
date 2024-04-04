import enum

from sqlalchemy import String, Column, Enum, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class UserRoleEnum(str, enum.Enum):
    super_admin = 'SUPER_ADMIN'
    admin = 'ADMIN'
    manager = 'MANAGER'


AVAILABLE_USER_ROLES = [UserRoleEnum.super_admin, UserRoleEnum.admin, UserRoleEnum.manager]


class User(Base):
    __tablename__ = 'users'

    provider_name = Column(String(255), nullable=True)
    provider_uid = Column(String(255), nullable=True)
    provider_id = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True, unique=True)
    encrypted_password = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), nullable=True)
    payload = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    is_disabled = Column(Boolean, default=False, nullable=False)
