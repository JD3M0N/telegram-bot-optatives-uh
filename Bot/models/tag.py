from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from bot.utils.db import Base

class Tag(Base):
    __tablename__ = "tags"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, nullable=False)

    # Backref a Course
    courses = relationship("Course", secondary="course_tag", back_populates="tags")
