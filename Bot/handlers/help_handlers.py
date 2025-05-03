# bot/handlers/help_handlers.py

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[HELP] Usuario {user.id} (@{user.username}) ejecuta /help")

    text = (
        "<b>🛠️ Comandos Generales</b>\n"
        "• <code>/start</code> – Inicia y registra tu cuenta.\n"
        "• <code>/menu</code> – Muestra el menú principal.\n"
        "• <code>/help</code> – Muestra esta guía.\n\n"

        "<b>👑 Admin</b>\n"
        "• <code>/promote &lt;telegram_id&gt;</code> – Promover a profesor.\n\n"

        "<b>🎓 Profesor</b>\n"
        "• <code>/addcourse</code> – Añadir un nuevo curso.\n"
        "• <code>/mycourses</code> – Ver tus cursos.\n"
        "• <code>/createtag</code> – Crear una nueva etiqueta.\n"
        "• <code>/addtag</code> – Asignar etiquetas a tus cursos.\n\n"

        "<b>👤 Estudiante</b>\n"
        "• <code>/selecttags</code> – Elegir tus intereses.\n"
        "• <code>/listoptativas</code> – Ver todas las optativas disponibles.\n"
        "• <code>/recomend</code> – Obtener hasta 10 recomendaciones.\n"
        "• <code>/info_&lt;id&gt;</code> – Ver detalles de una asignatura.\n"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
