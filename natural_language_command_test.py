from calendar_command import process_natural_language_command


mensajes = [
    "Recuérdame mañana a las 10:30 llevar el carro al taller",
    "Tengo una reunión el viernes a las 3 de la tarde",
    "Mañana a las 5 tengo que llevar el carro al taller",
    "Llevar el carro el lunes a las 8 de la mañana"
]


for mensaje in mensajes:

    print("\n" + "=" * 60)
    print("MENSAJE:", mensaje)
    print("=" * 60)

    resultado = process_natural_language_command(mensaje)

    print("\nRESPUESTA:")
    print(resultado)