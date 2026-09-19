from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


# ==========================================
# AUTENTICACIÓN
# ==========================================

flow = InstalledAppFlow.from_client_secrets_file(
    CREDENTIALS_FILE,
    SCOPES
)

credentials = flow.run_local_server(
    port=0
)


# ==========================================
# GUARDAR TOKEN
# ==========================================

with open(TOKEN_FILE, "w") as token:
    token.write(credentials.to_json())

print("\n✅ Token guardado correctamente.")


# ==========================================
# CONEXIÓN CON GOOGLE CALENDAR
# ==========================================

service = build(
    "calendar",
    "v3",
    credentials=credentials
)


# ==========================================
# LISTAR CALENDARIOS
# ==========================================

print("\n===== MIS CALENDARIOS =====")

calendar_list = service.calendarList().list().execute()

for calendar in calendar_list.get("items", []):
    print(
        f"- {calendar['summary']} "
        f"(ID: {calendar['id']})"
    )