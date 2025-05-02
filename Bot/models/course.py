from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from bot.utils.db import Base

# Tabla asociativa para la relación Course ↔ Tag
course_tag = Table(
    "course_tag",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
    Column("tag_id",    Integer, ForeignKey("tags.id"),    primary_key=True),
)

class Course(Base):
    __tablename__ = "courses"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String,  nullable=False)
    emoji       = Column(String(5), nullable=True)  
    description = Column(String)
    professor_id  = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación many-to-many con Tag
    tags    = relationship("Tag",    secondary=course_tag, back_populates="courses")
    # Relación one-to-many con Review
    reviews = relationship("Review", back_populates="course", cascade="all, delete-orphan")
    # Relación one-to-many con User (profesor)
    professor = relationship("User", back_populates="courses")  
