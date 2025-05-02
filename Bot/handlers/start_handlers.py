# bot/handlers/start_handlers.py
from telegram import Update
from telegram.ext import ContextTypes

# Funcion para /start con un mensaje de presentacion

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[START] Usuario {user.id} (@{user.username}) ejecuta /start")
    text = (
        "Hola, soy el bot de gestión de cursos optativos.\n"
        "Estoy aquí para ayudarte a gestionar asignaturas optativas, ya seas estudiante o profesor.\n\n"
        "Escribe /menu para ver los comandos disponibles segun tus privilegios.\n"
        "Escribe /help para ver la lista total de comandos disponibles."
    )
    await update.message.reply_text(text)