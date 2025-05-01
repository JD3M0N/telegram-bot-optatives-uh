# bot/handlers/menu_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.utils.db import SessionLocal
from bot.models.user import User

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
             InlineKeyboardButton("Añadir tag a curso",  callback_data="add_tag")]
        ],
        "professor": [
            [InlineKeyboardButton("Añadir curso",       callback_data="add_course"),
             InlineKeyboardButton("Añadir tag a curso", callback_data="add_tag")]
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
    user = query.from_user
    data = query.data
    print(f"[MENU CALLBACK] Usuario {user.id} (@{user.username}) pulsó: {data}")
    await query.answer()
    await query.edit_message_text(f"Has pulsado: {data}")
