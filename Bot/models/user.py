# bot/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm  import relationship
from bot.utils.db    import Base
import enum
from bot.models.tag import user_tag  

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

    # relaciones existentes…
    courses = relationship("Course", back_populates="professor")
    # nueva relación many-to-many con Tag
    tags    = relationship("Tag", secondary=user_tag, back_populates="users")