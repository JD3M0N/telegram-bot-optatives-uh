# bot/handlers/start_handlers.py

from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[START] Usuario {user.id} (@{user.username}) ejecuta /start") 

    text = (
        f"👋 *¡Hola, {user.first_name or user.username}!*\n\n"
        "🎓 *Bienvenido al OptativaUH Bot*\n"
        "Tu asistente para gestionar asignaturas optativas en la Universidad de La Habana.\n\n"
        "*¿Cómo empezar?*\n"
        "• Escribe /menu  para acceder al panel de opciones según tu rol.\n"
        "• Escribe /help  para ver todos los comandos disponibles.\n\n"
        "¡Empecemos! 🚀"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
