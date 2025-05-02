# bot/handlers/menu_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.db import SessionLocal
from bot.models.user import User
from bot.handlers.course_handlers import add_course_start, my_courses, create_tag_start, add_tag_start
from bot.handlers.student_handlers import list_optatives

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
            [InlineKeyboardButton("Crear etiqueta", callback_data="create_tag")],
            [InlineKeyboardButton("Añadir etiqueta a curso", callback_data="add_tag")],
        ],
        "professor": [
            [InlineKeyboardButton("Añadir curso",     callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso", callback_data="add_tag")],
            [InlineKeyboardButton("Mis cursos",       callback_data="my_courses")],
            [InlineKeyboardButton("Crear etiqueta", callback_data="create_tag")],
            [InlineKeyboardButton("Añadir etiqueta a curso", callback_data="add_tag")],
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
    query = update.callback_query
    data  = query.data
    user  = query.from_user
    await query.answer()

    if data == "add_course":
        print(f"[MENU CALLBACK] {user.id} pulsó Añadir curso → arrancando flujo")
        return await add_course_start(update, context)

    if data == "my_courses":
        print(f"[MENU CALLBACK] {user.id} pulsó Mis cursos")
        return await my_courses(update, context)

    if data == "create_tag":
        print(f"[MENU CALLBACK] {user.id} pulsó Crear etiqueta → arrancando flujo")
        return await create_tag_start(update, context)
    
    if data == "add_tag":
        print(f"[MENU CALLBACK] {user.id} pulsó Añadir etiqueta a curso → arrancando flujo")
        return await add_tag_start(update, context)
    
    if data == "list_optatives":
        print(f"[MENU CALLBACK] {user.id} pulsó Lista optativas")
        return await list_optatives(update, context)

    # cualquier otro callback…
    return await query.edit_message_text(f"Has pulsado: {data}")
