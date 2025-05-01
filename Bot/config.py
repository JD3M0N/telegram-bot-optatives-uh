# config.py
from dotenv import load_dotenv
import os

# load_dotenv()  # Busca automáticamente un .env en el directorio actual

# Asumiendo .env esta en la raiz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))



# Cargar las variables de entorno
BOT_TOKEN    = os.getenv("BOT_TOKEN")
# URL por defecto a SQLite en el fichero optativas.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///optativas.db")
# LOG_LEVEL    = os.getenv("LOG_LEVEL", "INFO")
