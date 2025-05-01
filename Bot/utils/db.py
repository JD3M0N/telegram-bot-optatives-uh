# bot/utils/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.config import DATABASE_URL

# 1) Definimos engine, SessionLocal y Base sin dependencias a modelos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # 1) Importa todos los modelos para registrar sus mappers
    import bot.models.user
    import bot.models.tag
    import bot.models.review
    import bot.models.course

    # 2) Crea las tablas
    Base.metadata.create_all(bind=engine)

    # 3) Inserta los admins por defecto
    from bot.models.user import User, RoleEnum
    db = SessionLocal()
    try:
        admin_ids = os.getenv("ADMIN_IDS", "")
        for tid in admin_ids.split(","):
            if not tid:
                continue
            telegram_id = int(tid)
            user = db.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(telegram_id=telegram_id, role=RoleEnum.admin)
                db.add(user)
        db.commit()
    finally:
        db.close()
