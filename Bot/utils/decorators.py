# bot/utils/decorators.py
from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.db import SessionLocal
from bot.models.user import User, RoleEnum

def admin_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        db = SessionLocal()
        try:
            tid = update.effective_user.id
            user = db.query(User).filter_by(telegram_id=tid).first()
            if not user or user.role != RoleEnum.admin:
                update.message.reply_text("🚫 Solo el admin puede usar este comando.")
                return
        finally:
            db.close()
        return func(update, context, *args, **kwargs)
    return wrapper

def professor_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        db = SessionLocal()
        try:
            tid = update.effective_user.id
            user = db.query(User).filter_by(telegram_id=tid).first()
            if not user or user.role not in (RoleEnum.professor, RoleEnum.admin):
                update.message.reply_text("🚫 Solo un profesor (o admin) puede usar este comando.")
                return
        finally:
            db.close()
        return func(update, context, *args, **kwargs)
    return wrapper