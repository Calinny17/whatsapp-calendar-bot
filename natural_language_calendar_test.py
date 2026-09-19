from natural_language_parser import parse_natural_language
from calendar_service import create_calendar_event


mensaje = "Recuérdame mañana a las 10:30 llevar el carro al taller"

print("=" * 60)
print("MENSAJE")
print("=" * 60)
print(mensaje)


resultado = parse_natural_language(mensaje)

print("\n" + "=" * 60)
print("PARSER")
print("=" * 60)
print(resultado)


if not resultado["success"]:
    print("\n❌ No se pudo interpretar el mensaje.")
    exit()


evento = create_calendar_event(
    title=resultado["description"],
    start_datetime=resultado["start_datetime"],
    description="Evento creado desde WhatsApp Calendar Bot.",
    duration_minutes=60
)


print("\n" + "=" * 60)
print("GOOGLE CALENDAR")
print("=" * 60)

print("✅ Evento creado correctamente.")
print("Título:", evento["summary"])
print("Inicio:", resultado["start_datetime"])
print("Enlace:", evento.get("htmlLink"))