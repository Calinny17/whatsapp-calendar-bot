from calendar_command import process_agenda_command


pruebas = [
    "hola",
    "ayuda",
    "/agendar",
    "/agendar 17/99/2026 11:00 Reunión",
    "/agendar 17/09/2026 Reunión",
    "quiero una cita",
]


for mensaje in pruebas:

    print("\n" + "=" * 60)
    print("MENSAJE:", mensaje)
    print("=" * 60)

    resultado = process_agenda_command(mensaje)

    print(resultado["message"])