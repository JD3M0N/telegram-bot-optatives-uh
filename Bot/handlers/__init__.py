# bot/handlers/__init__.py

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import ConversationHandler, MessageHandler, filters

from .admin_handlers    import promote_professor
from .course_handlers import (
    add_course_start,
    add_course_name,
    add_course_emoji,
    add_course_desc,
    add_course_cancel,
    my_courses,
    ASK_NAME, ASK_EMOJI, ASK_DESC
)
from .student_handlers  import select_tags, list_optatives
from .menu_handlers     import menu_handler, menu_callback_handler
from .help_handlers     import help_handler

def register_handlers(app):
    # Comandos de texto
    app.add_handler(CommandHandler("promote",       promote_professor))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("addcourse", add_course_start)],
        states={
            ASK_NAME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_name)],
            ASK_EMOJI: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_emoji)],
            ASK_DESC:  [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_desc)],
        },
        fallbacks=[CommandHandler("cancel", add_course_cancel)],
        name="addcourse_flow",
        allow_reentry=True
    ))
    # app.add_handler(CommandHandler("addtag",        add_tag))
    app.add_handler(CommandHandler("mycourses",     my_courses))  
    app.add_handler(CommandHandler("selecttags",    select_tags))
    app.add_handler(CommandHandler("listoptativas", list_optatives))
    app.add_handler(CommandHandler("help",  help_handler))
    app.add_handler(CommandHandler("menu",          menu_handler))

    # Callbacks de InlineKeyboard
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern="^menu$"))
