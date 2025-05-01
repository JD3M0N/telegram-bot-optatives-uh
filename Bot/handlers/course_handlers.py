# bot/handlers/course_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators import professor_only
from bot.utils.db import SessionLocal
from bot.models.course import Course
from bot.models.tag import Tag

@professor_only
async def add_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[PROFESSOR] Usuario {user.id} (@{user.username}) ejecuta /addcourse con args={context.args}")
    if not context.args:
        print("No se proporcionó nombre de curso.")
        return await update.message.reply_text("Uso: /addcourse <nombre del curso>")
    name = " ".join(context.args)
    db = SessionLocal()
    try:
        course = Course(name=name)
        db.add(course)
        db.commit()
        print(f"Curso '{name}' añadido con ID {course.id}.")
        await update.message.reply_text(f"✅ Curso '{name}' añadido.")
    except Exception as e:
        print(f"Error en add_course: {e}")
        await update.message.reply_text("❌ Error al añadir curso.")
    finally:
        db.close()

@professor_only
async def add_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[PROFESSOR] Usuario {user.id} (@{user.username}) ejecuta /addtag con args={context.args}")
    if len(context.args) < 2:
        print("No se proporcionó curso o etiqueta.")
        return await update.message.reply_text("Uso: /addtag <curso_id> <nombre de etiqueta>")
    try:
        course_id = int(context.args[0])
    except ValueError:
        print("ID de curso inválido.")
        return await update.message.reply_text("El ID de curso debe ser un número.")
    tag_name = " ".join(context.args[1:])
    db = SessionLocal()
    try:
        course = db.get(Course, course_id)
        if not course:
            print(f"Curso con ID {course_id} no encontrado.")
            return await update.message.reply_text(f"No existe un curso con ID {course_id}")
        tag = db.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        course.tags.append(tag)
        db.add(tag)
        db.commit()
        print(f"Etiqueta '{tag_name}' añadida al curso ID {course_id}.")
        await update.message.reply_text(f"✅ Etiqueta '{tag_name}' añadida al curso.")
    except Exception as e:
        print(f"Error en add_tag: {e}")
        await update.message.reply_text("❌ Error al añadir etiqueta.")
    finally:
        db.close()
