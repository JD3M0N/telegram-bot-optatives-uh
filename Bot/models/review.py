from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from bot.utils.db import Base

class Review(Base):
    __tablename__ = "reviews"

    id        = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id   = Column(Integer, ForeignKey("users.id"), nullable=False)  # Añadir ForeignKey a la tabla de usuarios
    year      = Column(Integer, nullable=False)
    rating    = Column(Integer, nullable=False)  # 1–5
    comment   = Column(Text)

    # Backref a Course
    course = relationship("Course", back_populates="reviews")
    # Backref a User/Student
    # user = relationship("User", back_populates="reviews")

    # Un estudiante no puede dejar más de una reseña por curso
    # __table_args__ = (
    #     UniqueConstraint('course_id', 'user_id', name='uix_user_course_review'),
    # )