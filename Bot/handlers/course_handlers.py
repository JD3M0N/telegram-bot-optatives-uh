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
from bot.models.tag import Tag
import string
import unicodedata

# region Cursos Opativos

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

async def my_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[MY COURSES] Usuario {user.id} (@{user.username}) ejecuta /mycourses")
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

    return await update.effective_message.reply_text(text, parse_mode="Markdown")

# endregion

# region Etiquetas

# Estado del ConversationHandler
ASK_TAG_NAME = 0

@professor_only
async def create_tag_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicio de /createtag o botón ‘createtag’."""
    user = update.effective_user
    print(f"[CREATE TAG] Inicio por {user.id} (@{user.username})")
    await update.effective_message.reply_text(
        "✏️ Escriba el nombre de la etiqueta que desea crear:"
    )
    return ASK_TAG_NAME

async def create_tag_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe el nombre, lo normaliza, verifica y crea la etiqueta."""
    raw = update.effective_message.text.strip()
    # Normalizar: minúsculas y quitar puntuación
    # 1) Pasar a minúsculas
    lower = raw.lower()

    # 2) Descomponer Unicode (NFD) y quitar marcas de acento (Mn)
    decomposed = unicodedata.normalize('NFD', lower)
    no_accents = ''.join(
        ch for ch in decomposed
        if unicodedata.category(ch) != 'Mn'
    )

    # 3) Quitar signos de puntuación
    normalized = ''.join(
        ch for ch in no_accents
        if ch not in string.punctuation
    )
    
    print(f"[CREATE TAG] Nombre recibido «{raw}», normalizado «{normalized}»")

    db = SessionLocal()
    try:
        exists = db.query(Tag).filter_by(name=normalized).first()
        if exists:
            print(f"[CREATE TAG] '{normalized}' ya existe (ID {exists.id})")
            await update.effective_message.reply_text(
                f"⚠️ La etiqueta «{normalized}» ya existe."
            )
        else:
            tag = Tag(name=normalized)
            db.add(tag)
            db.commit()
            print(f"[CREATE TAG] Etiqueta creada «{normalized}» (ID {tag.id})")
            await update.effective_message.reply_text(
                f"✅ Etiqueta «{normalized}» creada correctamente."
            )
    except Exception as e:
        print(f"[CREATE TAG] Error: {e}")
        await update.effective_message.reply_text(
            "❌ Hubo un error al crear la etiqueta."
        )
    finally:
        db.close()

    return ConversationHandler.END

async def create_tag_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela el flujo si se envía /cancel."""
    user = update.effective_user
    print(f"[CREATE TAG] Cancelado por {user.id} (@{user.username})")
    await update.effective_message.reply_text("⚠️ Operación cancelada.")
    return ConversationHandler.END
        
# endregion