# bot/handlers/student_handlers.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.utils.db import SessionLocal
from bot.models.course import Course
from bot.models.user import User
from bot.models.tag  import Tag


async def select_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} (@{user.username}) ejecuta /selecttags con args={context.args}")
    await update.message.reply_text("🔖 Función select_tags en desarrollo.")

async def list_optatives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"[STUDENT] Usuario {user.id} ejecuta /listoptativas")
    db = SessionLocal()
    try:
        cursos = db.query(Course).all()
    finally:
        db.close()

    if not cursos:
        return await update.message.reply_text("⚠️ No hay cursos disponibles.")

    # Construye una fila de botón por curso: callback_data="info_<id>"
    botones = [
        [InlineKeyboardButton(f"{c.emoji or ''} {c.name}", callback_data=f"info_{c.id}")]
        for c in cursos
    ]
    markup = InlineKeyboardMarkup(botones)

    await update.message.reply_text(
        "📚 *Cursos disponibles:*",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def course_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, str_id = query.data.split("_")
    course_id = int(str_id)

    db = SessionLocal()
    try:
        curso = db.query(Course).filter_by(id=course_id).first()
        if not curso:
            return await query.edit_message_text("⚠️ Curso no encontrado.")
        # ¡Carga aquí los tags mientras la sesión sigue viva!
        tags = [t.name for t in curso.tags]
    finally:
        db.close()

    tags_text = ", ".join(tags) if tags else "Sin etiquetas"
    texto = (
        f"*{curso.emoji or ''} {curso.name}*\n\n"
        f"*Descripción:* {curso.description}\n"
        f"*Etiquetas:* {tags_text}"
    )
    print(f"[STUDENT] Usuario {query.from_user.id} (@{query.from_user.username}")
    await query.edit_message_text(texto, parse_mode="Markdown")
    
    
    
async def my_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /mytags — lista las etiquetas que el estudiante ya tiene """
    tid = update.effective_user.id
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=tid).first()
        if not user or not user.tags:
            text = "⚠️ No tienes etiquetas seleccionadas."
        else:
            nombres = [t.name for t in user.tags]
            text = "🔖 *Tus etiquetas:*\n" + "\n".join(f"- {n}" for n in nombres)
    finally:
        db.close()
    await update.message.reply_text(text, parse_mode="Markdown")

def build_tags_markup(selected_ids: set[int], all_tags: list[Tag]) -> InlineKeyboardMarkup:
    """Construye el teclado con ✅ para añadir y ❌ para quitar."""
    buttons = []
    for tag in all_tags:
        # si NO está seleccionado, mostramos ✅ (para añadir)
        # si SÍ está seleccionado, mostramos ❌ (para quitar)
        icon = "✅" if tag.id not in selected_ids else "❌"
        buttons.append(
            InlineKeyboardButton(f"{icon} {tag.name}", callback_data=f"toggle_tag_{tag.id}")
        )
    # 2 botones por fila
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(keyboard)

async def select_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/selecttags — muestra todas las etiquetas con botones para añadir/quitar."""
    tid = update.effective_user.id
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=tid).first()
        selected_ids = {t.id for t in user.tags} if user else set()
        all_tags = db.query(Tag).order_by(Tag.name).all()
    finally:
        db.close()

    markup = build_tags_markup(selected_ids, all_tags)
    # si viene de /selecttags (mensaje), usamos reply_text
    if update.message:
        await update.message.reply_text(
            "🔖 Elige una etiqueta para añadir o quitar:",
            reply_markup=markup
        )
    # si viene de un callback (no debería llegar aquí normalmente), también lo cubrimos
    else:
        await update.callback_query.edit_message_text(
            "🔖 Elige una etiqueta para añadir o quitar:",
            reply_markup=markup
        )

async def toggle_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """CallbackQuery para añadir o quitar la etiqueta y refrescar el teclado."""
    query = update.callback_query
    await query.answer()  # quita el “relojito”

    tag_id = int(query.data.split("_")[-1])
    tid    = query.from_user.id

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=tid).first()
        tag  = db.query(Tag).get(tag_id)
        if not user or not tag:
            return await query.reply_text("❌ Usuario o etiqueta no encontrada.")

        if tag in user.tags:
            user.tags.remove(tag)
            print(f"[STUDENT] Usuario {user.telegram_id} quita tag {tag.name}")
            confirmation = f"❌ Se quitó «{tag.name}» de tu lista."
        else:
            user.tags.append(tag)
            print(f"[STUDENT] Usuario {user.telegram_id} añade tag {tag.name}")
            confirmation = f"✅ Se añadió «{tag.name}» a tu lista."
        db.commit()

        # preparamos el markup actualizado
        selected_ids = {t.id for t in user.tags}
        all_tags = db.query(Tag).order_by(Tag.name).all()
        new_markup = build_tags_markup(selected_ids, all_tags)

    finally:
        db.close()

    # 1) Editamos el mensaje original para refrescar botones
    await query.edit_message_text(
        "🔖 Elige una etiqueta para añadir o quitar:",
        reply_markup=new_markup
    )
    # 2) Enviamos un pequeño mensaje de confirmación
    await query.message.reply_text(confirmation)
    
async def recommend_optatives(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /recomend — Recomienda hasta 10 optativas según tus tags """
    tid = update.effective_user.id
    db  = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=tid).first()
        if not user:
            return await update.message.reply_text(
                "🚫 No estás registrado. Ejecuta primero /start."
            )

        # Tags seleccionadas por el estudiante
        selected_tag_ids = {t.id for t in user.tags}
        if not selected_tag_ids:
            return await update.message.reply_text(
                "⚠️ No tienes etiquetas. Usa /selecttags para elegir tus intereses."
            )

        # Calculamos cuántas etiquetas coinciden en cada curso
        scored = []
        for course in db.query(Course).all():
            course_tag_ids = {t.id for t in course.tags}
            match_count = len(selected_tag_ids & course_tag_ids)
            if match_count > 0:
                scored.append((course, match_count))

        if not scored:
            return await update.message.reply_text(
                "🔍 No encontramos optativas que coincidan con tus etiquetas."
            )

        # Ordenamos: primero mayor número de coincidencias, luego alfabético
        scored.sort(key=lambda x: (-x[1], x[0].name))
        top10 = [c for c, _ in scored[:10]]

        # Construimos el texto de respuesta
        lines = ["📚 *Los siguientes cursos optativos podrían interesarte:*"]
        for i, course in enumerate(top10, start=1):
            emoji = course.emoji or ""
            lines.append(f"{i}. {emoji} {course.name} `/info_{course.id}`")

        text = "\n".join(lines)
    finally:
        db.close()

    await update.message.reply_text(text, parse_mode="Markdown")