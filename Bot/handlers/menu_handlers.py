# bot/handlers/menu_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.db import SessionLocal
from bot.models.user import User
from bot.handlers.course_handlers import add_course_start, my_courses

def get_user_role(telegram_id: int) -> str:
    """Devuelve el rol del usuario ('admin', 'professor' o 'student')."""
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        return user.role.value if user else "student"
    finally:
        db.close()

def build_inline_menu(role: str) -> InlineKeyboardMarkup:
    """Construye el teclado inline de opciones según el rol."""
    options = {
        "admin": [
            [InlineKeyboardButton("Promover profes.", callback_data="promote")],
            [InlineKeyboardButton("Añadir curso",     callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso", callback_data="add_tag")],
            [InlineKeyboardButton("Mis cursos",       callback_data="my_courses")],
        ],
        "professor": [
            [InlineKeyboardButton("Añadir curso",     callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso", callback_data="add_tag")],
            [InlineKeyboardButton("Mis cursos",       callback_data="my_courses")],
        ],
        "student": [
            [InlineKeyboardButton("Seleccionar tags",   callback_data="select_tags")],
            [InlineKeyboardButton("Lista optativas",    callback_data="list_optatives")],
        ],
    }
    return InlineKeyboardMarkup(options.get(role, []))

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler de /menu: muestra el teclado inline según el rol del usuario."""
    user = update.effective_user
    print(f"[MENU] Usuario {user.id} (@{user.username}) ejecuta /menu")
    role   = get_user_role(user.id)
    markup = build_inline_menu(role)
    await update.message.reply_text("Elige una opción:", reply_markup=markup)

async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Procesa los callbacks del menú inline:
      - add_course    → arranca el ConversationHandler de añadir curso
      - my_courses    → lista los cursos del profesor
      - cualquier otro → muestra el callback_data
    """
    query = update.callback_query
    data  = query.data
    user  = query.from_user
    await query.answer()  # cierra el spinner del botón

    if data == "add_course":
        print(f"[MENU CALLBACK] Usuario {user.id} pulsó Añadir curso")
        # Delegamos al flujo de conversación de add_course
        return await add_course_start(update, context)

    if data == "my_courses":
        print(f"[MENU CALLBACK] Usuario {user.id} pulsó Mis cursos")
        # Delegamos al handler que muestra los cursos del profesor
        return await my_courses(update, context)

    # Para cualquier otro callback, lo mostramos directamente
    print(f"[MENU CALLBACK] Usuario {user.id} pulsó: {data}")
    return await query.edit_message_text(f"Has pulsado: {data}")
