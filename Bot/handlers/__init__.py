# bot/handlers/__init__.py

from telegram.ext import CommandHandler, CallbackQueryHandler

from .admin_handlers    import promote_professor
from .course_handlers   import add_course, add_tag
from .student_handlers  import select_tags, list_optatives
from .menu_handlers     import menu_handler, menu_callback_handler
from .help_handlers     import help_handler

def register_handlers(app):
    # Comandos de texto
    app.add_handler(CommandHandler("promote",       promote_professor))
    app.add_handler(CommandHandler("addcourse",     add_course))
    app.add_handler(CommandHandler("addtag",        add_tag))
    app.add_handler(CommandHandler("selecttags",    select_tags))
    app.add_handler(CommandHandler("listoptativas", list_optatives))
    app.add_handler(CommandHandler("help",  help_handler))
    app.add_handler(CommandHandler("menu",          menu_handler))

    # Callbacks de InlineKeyboard
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern="^menu$"))
