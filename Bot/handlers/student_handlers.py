# bot/handlers/student_handlers.py
from telegram import Update
from telegram.ext import ContextTypes

async def select_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} (@{user.username}) ejecuta /selecttags con args={context.args}")
    await update.message.reply_text("🔖 Función select_tags en desarrollo.")

async def list_optatives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} (@{user.username}) ejecuta /listoptativas")
    await update.message.reply_text("📚 Función listoptativas en desarrollo.")
