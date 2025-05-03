# bot/handlers/start_handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.db    import SessionLocal
from bot.models.user import User, RoleEnum

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_telegram = update.effective_user
    print(f"[START] Usuario {user_telegram.id} (@{user_telegram.username}) ejecuta /start")

    # —––––— Registro o actualización del usuario —––––—
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=user_telegram.id).first()
        if not user:
            # Si no existe, lo creamos con rol student por defecto
            user = User(
                telegram_id=user_telegram.id,
                username   = user_telegram.username,
                role       = RoleEnum.student
            )
            db.add(user)
            db.commit()
    finally:
        db.close()

    # —––––— Mensaje de bienvenida —––––—
    text = (
        f"👋 ¡Hola, {user_telegram.first_name or user_telegram.username}!\n\n"
        "🎓 *Bienvenido al OptativaUH Bot*\n"
        "Tu asistente para gestionar asignaturas optativas.\n\n"
        "• Escribe /menu  para ver tus opciones.\n"
        "• Escribe /help  para la lista completa de comandos."
    )
    await update.message.reply_text(text, parse_mode="Markdown")
