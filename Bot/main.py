# bot/main.py

import os
from dotenv import load_dotenv

from bot.utils.db import init_db
from bot.handlers import register_handlers

# Importa el nuevo builder
from telegram.ext import ApplicationBuilder

import warnings
from telegram.warnings import PTBUserWarning

# Suprime todos los PTBUserWarning relacionados con CallbackQueryHandler
warnings.filterwarnings(
    "ignore",
    message=r".*CallbackQueryHandler.*",
    category=PTBUserWarning
)

# 1) Carga .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    # 2) Inicializa la base de datos
    init_db()
    print("✅ Base de datos inicializada.")

    # 3) Construye la aplicación (remplaza a Updater)
    app = ApplicationBuilder()\
        .token(BOT_TOKEN)\
        .build()
    print("✅ Bot de Telegram inicializado.")

    # 4) Registra tus handlers en la app
    register_handlers(app)
    print("✅ Handlers registrados.")

    # 5) Arranca el bot
    print("🤖 Bot está escuchando actualizaciones…")
    app.run_polling()

if __name__ == "__main__":
    print("▶️ Arrancando el bot…")
    main()
