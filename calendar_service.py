from pathlib import Path
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """
    Conecta con Google Calendar utilizando el token guardado.
    """

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    service = build(
        "calendar",
        "v3",
        credentials=credentials
    )

    return service


def create_calendar_event(
    title,
    start_datetime,
    description="",
    duration_minutes=60,
    timezone="America/Tijuana"
):
    """
    Crea un evento en el calendario principal.

    Parámetros:
        title: título del evento
        start_datetime: fecha y hora de inicio
        description: descripción del evento
        duration_minutes: duración en minutos
        timezone: zona horaria
    """

    service = get_calendar_service()

    end_datetime = start_datetime + timedelta(
        minutes=duration_minutes
    )

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_datetime.isoformat(),
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_datetime.isoformat(),
            "timeZone": timezone
        }
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return created_event