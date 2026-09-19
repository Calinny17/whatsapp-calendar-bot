from command_parser import parse_agenda_command
from calendar_service import create_calendar_event
from natural_language_parser import parse_natural_language


def process_agenda_command(text):
    """
    Procesa los mensajes recibidos desde WhatsApp.

    Reconoce:
    - Mensajes normales
    - Ayuda
    - Comandos /agendar
    - Errores específicos del comando
    """

    text = text.strip()
    text_lower = text.lower()

    # ==========================================
    # MENSAJES NORMALES
    # ==========================================

    if text_lower in [
        "hola",
        "hello",
        "buenas",
        "buenos días",
        "buenas tardes",
        "buenas noches"
    ]:
        return {
            "success": False,
            "message": (
                "👋 ¡Hola!\n\n"
                "Soy tu asistente de calendario.\n\n"
                "Puedo ayudarte a crear eventos en Google Calendar.\n\n"
                "Por ejemplo:\n"
                "/agendar 17/09/2026 11:00 Llevar el carro al taller\n\n"
                "Escribe *ayuda* para ver más información."
            )
        }

    # ==========================================
    # AYUDA
    # ==========================================

    if text_lower in ["ayuda", "help", "/ayuda", "/help"]:
        return {
            "success": False,
            "message": (
                "📅 *Ayuda - WhatsApp Calendar Bot*\n\n"
                "Por ahora puedo crear eventos en Google Calendar.\n\n"
                "📝 Usa este formato:\n"
                "/agendar DD/MM/YYYY HH:MM descripción\n\n"
                "Ejemplo:\n"
                "/agendar 20/09/2026 18:30 Cita con el dentista\n\n"
                "También puedes escribirme *hola* para comenzar."
            )
        }

    # ==========================================
    # COMANDO /AGENDAR
    # ==========================================

    if text_lower.startswith("/agendar"):

        command = parse_agenda_command(text)

        # --------------------------------------
        # Error inesperado / comando no válido
        # --------------------------------------

        if command is None:
            return {
                "success": False,
                "message": (
                    "⚠️ No reconozco ese comando.\n\n"
                    "Usa:\n"
                    "/agendar DD/MM/YYYY HH:MM descripción\n\n"
                    "Ejemplo:\n"
                    "/agendar 17/09/2026 11:00 Llevar el carro al taller"
                )
            }

        # --------------------------------------
        # Errores específicos del parser
        # --------------------------------------

        if command["success"] is False:

            error = command["error"]

            if error == "missing_data":
                message = (
                    "⚠️ El comando /agendar necesita más información.\n\n"
                    "Usa:\n"
                    "/agendar DD/MM/YYYY HH:MM descripción\n\n"
                    "Ejemplo:\n"
                    "/agendar 17/09/2026 11:00 Llevar el carro al taller"
                )

            elif error == "missing_date":
                message = (
                    "⚠️ Falta la fecha del evento.\n\n"
                    "Usa el formato:\n"
                    "/agendar DD/MM/YYYY HH:MM descripción"
                )

            elif error == "missing_time":
                message = (
                    "⚠️ Falta la hora del evento.\n\n"
                    "Usa el formato:\n"
                    "/agendar DD/MM/YYYY HH:MM descripción"
                )

            elif error == "missing_description":
                message = (
                    "⚠️ Falta la descripción del evento.\n\n"
                    "Por ejemplo:\n"
                    "/agendar 17/09/2026 11:00 Llevar el carro al taller"
                )

            elif error == "invalid_date":
                message = (
                    "⚠️ La fecha no es válida.\n\n"
                    "Usa el formato:\n"
                    "DD/MM/YYYY\n\n"
                    "Ejemplo:\n"
                    "17/09/2026"
                )

            elif error == "invalid_time":
                message = (
                    "⚠️ La hora no es válida.\n\n"
                    "Usa el formato:\n"
                    "HH:MM\n\n"
                    "Ejemplo:\n"
                    "11:00"
                )

            else:
                message = (
                    "⚠️ No pude interpretar el comando.\n\n"
                    "Escribe *ayuda* para ver el formato correcto."
                )

            return {
                "success": False,
                "message": message
            }

        # ======================================
        # CREAR EVENTO
        # ======================================

        evento = create_calendar_event(
            title=command["description"],
            start_datetime=command["start_datetime"],
            description="Evento creado desde WhatsApp Calendar Bot.",
            duration_minutes=60
        )

        return {
            "success": True,
            "message": (
                "✅ Evento creado correctamente.\n\n"
                f"📅 {command['start_datetime'].strftime('%d/%m/%Y')}\n"
                f"🕐 {command['start_datetime'].strftime('%H:%M')}\n"
                f"📝 {command['description']}\n\n"
                f"🔗 {evento.get('htmlLink')}"
            )
        }

    # ==========================================
    # MENSAJE DESCONOCIDO
    # ==========================================

    return {
        "success": False,
        "message": (
            "🤔 No estoy seguro de lo que quieres hacer.\n\n"
            "Actualmente puedo crear eventos en Google Calendar.\n\n"
            "Usa:\n"
            "/agendar DD/MM/YYYY HH:MM descripción\n\n"
            "Ejemplo:\n"
            "/agendar 18/09/2026 09:00 Reunión de trabajo\n\n"
            "Escribe *ayuda* para ver las instrucciones."
        )
    }
    
def process_natural_language_command(text):
    """
    Procesa un mensaje escrito en lenguaje natural
    y crea un evento en Google Calendar.
    """

    resultado = parse_natural_language(text)

    if not resultado["success"]:

        if resultado["error"] == "date_not_found":
            return {
                "success": False,
                "message": (
                    "⚠️ No pude encontrar una fecha en tu mensaje.\n\n"
                    "Por ejemplo:\n"
                    "Recuérdame mañana a las 10:30 llevar el carro al taller"
                )
            }
        
        if resultado["error"] == "ambiguous_time":
            return {
                "success": False,
                "message": (
                    "⚠️ La hora que indicaste es ambigua.\n\n"
                    "Por favor especifica si es por la mañana, "
                    "por la tarde o por la noche.\n\n"
                    "Ejemplos:\n"
                    "• Mañana a las 5 de la tarde llevar el carro al taller\n"
                    "• Mañana a las 5 de la mañana llevar el carro al taller\n"
                    "• Mañana a las 17:00 llevar el carro al taller"
                )
            }

        if resultado["error"] == "time_not_found":
            return {
                "success": False,
                "message": (
                    "⚠️ No pude encontrar una hora en tu mensaje.\n\n"
                    "Por ejemplo:\n"
                    "Recuérdame mañana a las 10:30 llevar el carro al taller"
                )
            }

        if resultado["error"] == "description_not_found":
            return {
                "success": False,
                "message": (
                    "⚠️ No pude encontrar qué quieres agendar.\n\n"
                    "Por ejemplo:\n"
                    "Recuérdame mañana a las 10:30 llevar el carro al taller"
                )
            }

        return {
            "success": False,
            "message": (
                "⚠️ No pude interpretar el mensaje.\n\n"
                "Escribe *ayuda* para ver ejemplos."
            )
        }

    evento = create_calendar_event(
        title=resultado["description"],
        start_datetime=resultado["start_datetime"],
        description="Evento creado desde WhatsApp Calendar Bot.",
        duration_minutes=60
    )

    return {
        "success": True,
        "message": (
            "✅ Evento creado correctamente.\n\n"
            f"📅 {resultado['start_datetime'].strftime('%d/%m/%Y')}\n"
            f"🕐 {resultado['start_datetime'].strftime('%H:%M')}\n"
            f"📝 {resultado['description']}\n\n"
            f"🔗 {evento.get('htmlLink')}"
        )
    }