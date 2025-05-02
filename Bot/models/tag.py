from sqlalchemy import Table, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from bot.utils.db import Base



# tabla asociativa User ↔ Tag
user_tag = Table(
    "user_tag",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("tag_id",  Integer, ForeignKey("tags.id"),   primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, nullable=False)

    # backref a usuarios
    users = relationship("User", secondary="user_tag", back_populates="tags")
    # backref a cursos (existente)
    courses = relationship("Course", secondary="course_tag", back_populates="tags")