# bot/handlers/menu_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.utils.db import SessionLocal
from bot.models.user import User
from bot.models.course import Course

def get_user_role(telegram_id: int) -> str:
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        return user.role.value if user else "student"
    finally:
        db.close()

def build_inline_menu(role: str) -> InlineKeyboardMarkup:
    options = {
        "admin": [
            [InlineKeyboardButton("Promover profes.",    callback_data="promote")],
            [InlineKeyboardButton("Añadir curso",        callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso",  callback_data="add_tag")],
            [InlineKeyboardButton("Mis cursos",         callback_data="my_courses")],
        ],
        "professor": [
            [InlineKeyboardButton("Añadir curso",       callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso", callback_data="add_tag")],
            [InlineKeyboardButton("Mis cursos",        callback_data="my_courses")],
        ],
        "student": [
            [InlineKeyboardButton("Seleccionar tags",   callback_data="select_tags")],
            [InlineKeyboardButton("Lista de optativas", callback_data="list_optatives")]
        ]
    }
    return InlineKeyboardMarkup(options.get(role, []))

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[MENU] Usuario {user.id} (@{user.username}) ejecuta /menu")
    role = get_user_role(user.id)
    markup = build_inline_menu(role)
    await update.message.reply_text("Elige una opción:", reply_markup=markup)
    
    
async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data  = query.data
    user  = query.from_user
    await query.answer()

    if data == "mycourses":
        print(f"[MENU CALLBACK] {user.id} pulsó Mis cursos")
        db = SessionLocal()
        try:
            # localiza al profesor en la BD
            prof = db.query(User).filter_by(telegram_id=user.id).first()
            # obtiene sus cursos
            cursos = db.query(Course).filter_by(professor_id=prof.id).all() if prof else []
        finally:
            db.close()

        if not cursos:
            text = "⚠️ No tienes cursos registrados."
        else:
            lineas = [f"{c.emoji or ''} {c.name} (ID: {c.id})" for c in cursos]
            text   = "📚 *Tus cursos:*\n" + "\n".join(lineas)

        return await query.edit_message_text(text, parse_mode="Markdown")

    # --- resto de callbacks ya existentes ---
    print(f"[MENU CALLBACK] {user.id} pulsó: {data}")
    return await query.edit_message_text(f"Has pulsado: {data}")