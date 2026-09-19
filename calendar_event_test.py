from pathlib import Path
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


# ==========================================
# AUTENTICACIÓN
# ==========================================

credentials = Credentials.from_authorized_user_file(
    TOKEN_FILE,
    SCOPES
)


# ==========================================
# CONEXIÓN CON GOOGLE CALENDAR
# ==========================================

service = build(
    "calendar",
    "v3",
    credentials=credentials
)


# ==========================================
# EVENTO DE PRUEBA
# ==========================================

inicio = datetime.now() + timedelta(minutes=10)
fin = inicio + timedelta(hours=1)

evento = {
    "summary": "Prueba WhatsApp Calendar Bot",
    "description": "Evento creado automáticamente desde Python.",
    "start": {
        "dateTime": inicio.isoformat(),
        "timeZone": "America/Tijuana",
    },
    "end": {
        "dateTime": fin.isoformat(),
        "timeZone": "America/Tijuana",
    },
}


# ==========================================
# CREAR EVENTO
# ==========================================

evento_creado = service.events().insert(
    calendarId="primary",
    body=evento
).execute()


print("\n===== EVENTO CREADO =====")
print("Título:", evento_creado["summary"])
print("Inicio:", evento_creado["start"]["dateTime"])
print("Fin:", evento_creado["end"]["dateTime"])
print("Enlace:", evento_creado.get("htmlLink"))