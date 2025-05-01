# bot/handlers/help_handlers.py
from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[HELP] Usuario {user.id} (@{user.username}) ejecuta /help")
    text = (
        "/start         – Inicia y registra al usuario\n"
        "/menu          – Muestra el menú según tu rol (admin/professor/student)\n"
        "/help          – Muestra esta ayuda\n\n"
        "👑 admin:\n"
        "  /promote      – Promover estudiante a profesor\n\n"
        "🎓 professor:\n"
        "  /addcourse    – Añadir un nuevo curso\n"
        "  /addtag       – Añadir etiqueta a un curso\n\n"
        "👤 student:\n"
        "  /selecttags   – Seleccionar tus tags de interés\n"
        "  /listoptativas– Ver lista de asignaturas recomendadas"
    )
    await update.message.reply_text(text)
