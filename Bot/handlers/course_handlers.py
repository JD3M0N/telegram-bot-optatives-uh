from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from bot.utils.decorators import professor_only
from bot.utils.db import SessionLocal
from bot.models.course import Course
from bot.models.user import User

# Estados del ConversationHandler
ASK_NAME, ASK_EMOJI, ASK_DESC = range(3)

@professor_only
async def add_course_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[ADD COURSE] Inicio por {update.effective_user.id}")
    await update.message.reply_text("✏️ Por favor, escribe el *nombre* del nuevo curso:", parse_mode="Markdown")
    return ASK_NAME

async def add_course_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["new_course_name"] = name
    print(f"[ADD COURSE] Nombre recibido: {name}")
    await update.message.reply_text("🎨 Ahora envía el *emoji* que representará al curso:", parse_mode="Markdown")
    return ASK_EMOJI

async def add_course_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emoji = update.message.text.strip()
    context.user_data["new_course_emoji"] = emoji
    print(f"[ADD COURSE] Emoji recibido: {emoji}")
    await update.message.reply_text("📝 Finalmente, escribe la *descripción* del curso:", parse_mode="Markdown")
    return ASK_DESC

async def add_course_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    desc = update.message.text.strip()
    name  = context.user_data["new_course_name"]
    emoji = context.user_data["new_course_emoji"]
    print(f"[ADD COURSE] Descripción recibida: {desc}")

    db = SessionLocal()
    try:
        # localiza al profesor en la BD por telegram_id
        prof = db.query(User).filter_by(telegram_id=update.effective_user.id).first()
        course = Course(
            name=name,
            emoji=emoji,
            description=desc,
            professor_id=prof.id
        )
        db.add(course)
        db.commit()
        print(f"[ADD COURSE] Curso creado: {emoji} {name} (ID {course.id}) por prof_id={prof.id}")
        await update.message.reply_text(
            f"✅ Curso *{emoji} {name}* añadido correctamente.\n"
            f"Descripción: {desc}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"[ADD COURSE] Error al guardar en BD: {e}")
        await update.message.reply_text("❌ Hubo un error al crear el curso.")
    finally:
        db.close()

    return ConversationHandler.END

async def add_course_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[ADD COURSE] Cancelado por {update.effective_user.id}")
    await update.message.reply_text("⚠️ Operación cancelada.")
    return ConversationHandler.END
