from datetime import datetime


def parse_agenda_command(text):
    """
    Interpreta un comando con el formato:

    /agendar DD/MM/YYYY HH:MM descripción

    Devuelve los datos del evento o un error específico.
    """

    parts = text.strip().split(maxsplit=3)

    # ------------------------------------------
    # Comando incompleto
    # ------------------------------------------

    if len(parts) == 1:
        return {
            "success": False,
            "error": "missing_data"
        }

    # ------------------------------------------
    # Verificar comando
    # ------------------------------------------

    command = parts[0].lower()

    if command != "/agendar":
        return None

    # ------------------------------------------
    # Falta fecha
    # ------------------------------------------

    if len(parts) < 2:
        return {
            "success": False,
            "error": "missing_date"
        }

    date_text = parts[1]

    # ------------------------------------------
    # Falta hora
    # ------------------------------------------

    if len(parts) < 3:
        return {
            "success": False,
            "error": "missing_time"
        }

    time_text = parts[2]

    # ------------------------------------------
    # Validar que realmente sea una hora
    # ------------------------------------------

    try:
        datetime.strptime(time_text, "%H:%M")

    except ValueError:
        return {
            "success": False,
            "error": "missing_time"
        }

    # ------------------------------------------
    # Falta descripción
    # ------------------------------------------

    if len(parts) < 4:
        return {
            "success": False,
            "error": "missing_description"
        }

    description = parts[3].strip()

    if not description:
        return {
            "success": False,
            "error": "missing_description"
        }

    # ------------------------------------------
    # Validar fecha
    # ------------------------------------------

    try:
        start_datetime = datetime.strptime(
            f"{date_text} {time_text}",
            "%d/%m/%Y %H:%M"
        )

    except ValueError:
        return {
            "success": False,
            "error": "invalid_date"
        }

    # ------------------------------------------
    # Comando válido
    # ------------------------------------------

    return {
        "success": True,
        "start_datetime": start_datetime,
        "description": description
    }