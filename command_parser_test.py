from command_parser import parse_agenda_command


mensaje = "/agendar 15/09/2026 10:30 Llevar el carro al taller"

resultado = parse_agenda_command(mensaje)

print("\n===== RESULTADO =====")
print("Fecha y hora:", resultado["start_datetime"])
print("Descripción:", resultado["description"])