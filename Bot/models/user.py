# bot/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm  import relationship
from bot.utils.db    import Base
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

    # ← Añade esto para que Course.professor ↔ User.courses funcione
    courses = relationship("Course", back_populates="professor")

    # Si también usas reviews:
    # reviews = relationship("Review", back_populates="user")
