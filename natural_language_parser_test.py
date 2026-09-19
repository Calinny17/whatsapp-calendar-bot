from natural_language_parser import parse_natural_language


mensajes = [
    "Recuérdame mañana a las 10:30 llevar el carro al taller",
    "Tengo una reunión el viernes a las 3 de la tarde",
    "Llevar el carro el lunes a las 8 de la mañana",
    "Pagar la luz el sábado a las 18:30",
    "Ir al banco el domingo a las 12:00",
    "Mañana a las 5 tengo que llevar el carro al taller",
    "Tengo una cita mañana",
    "Tengo que hacer algo después a las 10:30",
    "Recuérdame mañana a las 5 pm llevar el carro al taller",
    "Recuérdame mañana a las 5 p.m. llevar el carro al taller",
    "Recuérdame mañana a las 5 am ir al gimnasio",
    "Recuérdame mañana a las 5 a.m. ir al gimnasio",
    "Recuérdame mañana al mediodía pagar la comida",
    "Recuérdame mañana a medianoche revisar el sistema"
]


for mensaje in mensajes:
    print("\n" + "=" * 60)
    print("MENSAJE:", mensaje)
    print("=" * 60)

    resultado = parse_natural_language(mensaje)

    print("RESULTADO:", resultado)