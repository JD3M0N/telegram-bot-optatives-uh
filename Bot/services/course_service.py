from bot.utils.db import SessionLocal
from bot.models.course import Course

def create_course(name: str, description: str, professor: str):
    db = SessionLocal()
    try:
        curso = Course(name=name, description=description, professor=professor)
        db.add(curso)
        db.commit()
        db.refresh(curso)
        return curso
    finally:
        db.close()

def list_courses():
    db = SessionLocal()
    try:
        return db.query(Course).all()
    finally:
        db.close()
