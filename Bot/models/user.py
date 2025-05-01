from sqlalchemy import Column, Integer, String, Enum
from bot.utils.db import Base
import enum

class RoleEnum(enum.Enum):
    admin     = "admin"
    professor = "professor"
    student   = "student"

class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username    = Column(String, nullable=True)
    role        = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False)
