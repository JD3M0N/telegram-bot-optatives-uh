# bot/handlers/admin_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators import admin_only
from bot.utils.db import SessionLocal
from bot.models.user import User, RoleEnum

@admin_only
async def promote_professor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[ADMIN] Usuario {user.id} (@{user.username}) ejecuta /promote con args={context.args}")
    db = SessionLocal()
    try:
        if not context.args:
            print("No se proporcionó el ID de usuario.")
            return await update.message.reply_text("Uso: /promote <telegram_id>")
        target_id = int(context.args[0])
        db_user = db.query(User).filter_by(telegram_id=target_id).first()
        if not db_user:
            db_user = User(telegram_id=target_id, role=RoleEnum.professor)
            db.add(db_user)
        else:
            db_user.role = RoleEnum.professor
        db.commit()
        print(f"Usuario {target_id} promovido a profesor.")
        await update.message.reply_text(f"✅ Usuario {target_id} promovido a profesor.")
    except Exception as e:
        print(f"Error en promote_professor: {e}")
        await update.message.reply_text("❌ Error al promover profesor.")
    finally:
        db.close()
