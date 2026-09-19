from datetime import datetime, timedelta

from calendar_service import create_calendar_event


inicio = datetime.now() + timedelta(minutes=10)


evento = create_calendar_event(
    title="Prueba función Calendar Service",
    start_datetime=inicio,
    description="Prueba de la función reutilizable.",
    duration_minutes=30
)


print("\n===== EVENTO CREADO =====")
print("Título:", evento["summary"])
print("Inicio:", evento["start"]["dateTime"])
print("Fin:", evento["end"]["dateTime"])
print("Enlace:", evento.get("htmlLink"))