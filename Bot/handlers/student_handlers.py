# bot/handlers/student_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.utils.db import SessionLocal
from bot.models.course import Course


async def select_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} (@{user.username}) ejecuta /selecttags con args={context.args}")
    await update.message.reply_text("🔖 Función select_tags en desarrollo.")

async def list_optatives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} ejecuta /listoptativas")
    db = SessionLocal()
    try:
        cursos = db.query(Course).all()
    finally:
        db.close()

    if not cursos:
        return await update.message.reply_text("⚠️ No hay cursos disponibles.")

    # Construye una fila de botón por curso: callback_data="info_<id>"
    botones = [
        [InlineKeyboardButton(f"{c.emoji or ''} {c.name}", callback_data=f"info_{c.id}")]
        for c in cursos
    ]
    markup = InlineKeyboardMarkup(botones)

    await update.message.reply_text(
        "📚 *Cursos disponibles:*",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def course_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, str_id = query.data.split("_")
    course_id = int(str_id)

    db = SessionLocal()
    try:
        curso = db.query(Course).filter_by(id=course_id).first()
        if not curso:
            return await query.edit_message_text("⚠️ Curso no encontrado.")
        # ¡Carga aquí los tags mientras la sesión sigue viva!
        tags = [t.name for t in curso.tags]
    finally:
        db.close()

    tags_text = ", ".join(tags) if tags else "Sin etiquetas"
    texto = (
        f"*{curso.emoji or ''} {curso.name}*\n\n"
        f"*Descripción:* {curso.description}\n"
        f"*Etiquetas:* {tags_text}"
    )
    print(f"[STUDENT] Usuario {query.from_user.id} (@{query.from_user.username}) "
    await query.edit_message_text(texto, parse_mode="Markdown")