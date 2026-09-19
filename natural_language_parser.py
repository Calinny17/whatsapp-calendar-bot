from datetime import datetime, timedelta
import re


def detect_date(text):
    """
    Detecta una fecha básica dentro de un mensaje
    escrito en lenguaje natural.
    """

    text = text.lower()

    hoy = datetime.now().date()

    # Primero comprobamos expresiones específicas
    # para evitar conflictos con palabras como "mañana".

    if "pasado mañana" in text:
        return hoy + timedelta(days=2)

    # "mañana" debe ser una palabra independiente.
    # Así evitamos confundir "8 de la mañana"
    # con "mañana" como fecha.
    if re.search(r"\bmañana\b", text) and "de la mañana" not in text:
        return hoy + timedelta(days=1)

    if re.search(r"\bhoy\b", text):
        return hoy

    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }

    for dia, numero_dia in dias_semana.items():
        if re.search(rf"\b{dia}\b", text):
            dias_hasta = (numero_dia - hoy.weekday()) % 7

            if dias_hasta == 0:
                dias_hasta = 7

            return hoy + timedelta(days=dias_hasta)

    return None

def detect_time(text):
    """
    Detecta una hora dentro de un mensaje
    escrito en lenguaje natural.

    Devuelve:
    - (hora, minutos) si la hora es clara.
    - "ambiguous" si se encontró una hora sin
      indicar AM/PM o periodo.
    - None si no se encontró ninguna hora.
    """

    text = text.lower()

    # -------------------------------------------------
    # 1. Mediodía y medianoche
    # -------------------------------------------------

    if re.search(r"\b(al\s+)?mediodía\b", text):
        return 12, 0

    if re.search(r"\b(a\s+)?medianoche\b", text):
        return 0, 0

    # -------------------------------------------------
    # 2. Formato HH:MM
    # -------------------------------------------------

    match = re.search(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        text
    )

    if match:
        hora = int(match.group(1))
        minutos = int(match.group(2))

        return hora, minutos

    # -------------------------------------------------
    # 3. Formato AM / PM
    #
    # Ejemplos:
    # 5 am
    # 5 pm
    # 5 a.m.
    # 5 p.m.
    # -------------------------------------------------

    match = re.search(
        r"\b([1-9]|1[0-2])\s*(a\.?m\.?|p\.?m\.?)\b",
        text
    )

    if match:
        hora = int(match.group(1))
        periodo = match.group(2).replace(".", "")

        if periodo == "am":
            if hora == 12:
                hora = 0

        elif periodo == "pm":
            if hora != 12:
                hora += 12

        return hora, 0

    # -------------------------------------------------
    # 4. Formato "X de la mañana/tarde/noche"
    # -------------------------------------------------

    match = re.search(
        r"\b([1-9]|1[0-2])\s+de\s+la\s+(mañana|tarde|noche)\b",
        text
    )

    if match:
        hora = int(match.group(1))
        periodo = match.group(2)

        if periodo == "mañana":
            if hora == 12:
                hora = 0

        elif periodo == "tarde":
            if hora != 12:
                hora += 12

        elif periodo == "noche":
            if hora != 12:
                hora += 12

        return hora, 0

    # -------------------------------------------------
    # 5. Hora sin AM/PM
    #
    # Ejemplos:
    # a las 5
    # a las 8
    # a las 11
    #
    # No adivinamos AM/PM.
    # -------------------------------------------------

    match = re.search(
        r"\ba\s+las\s+([1-9]|1[0-2])\b",
        text
    )

    if match:
        return "ambiguous"

    # -------------------------------------------------
    # 6. No se encontró ninguna hora
    # -------------------------------------------------

    return None


def extract_description(text):
    """
    Extrae la descripción del evento
    eliminando las expresiones de fecha y hora.
    """

    descripcion = text.lower().strip()

    # -------------------------------------------------
    # 1. Eliminar expresiones completas de hora
    # -------------------------------------------------

    # Ejemplos:
    # 10:30
    # 18:30
    # 8:00
    descripcion = re.sub(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        "",
        descripcion
    )

    # Ejemplos:
    # 3 de la tarde
    # 8 de la mañana
    # 10 de la noche
    descripcion = re.sub(
        r"\b([1-9]|1[0-2])\s*(a\.?m\.?|p\.?m\.?)\.?",
        "",
        descripcion
    )
    
    # -------------------------------------------------
    # Eliminar expresiones AM / PM
    # -------------------------------------------------

    # Ejemplos:
    # 5 am
    # 5 pm
    # 5 a.m.
    #5 p.m.

    descripcion = re.sub(
        r"\b([1-9]|1[0-2])\s*(a\.?m\.?|p\.?m\.?)\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # Eliminar mediodía y medianoche
    # -------------------------------------------------

    descripcion = re.sub(
        r"\b(al\s+)?mediodía\b",
        "",
        descripcion
    )

    descripcion = re.sub(
        r"\b(a\s+)?medianoche\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 2. Eliminar expresiones de fecha
    # -------------------------------------------------

    expresiones_fecha = [
        "pasado mañana",
        "mañana",
        "hoy",
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    for expresion in expresiones_fecha:
        descripcion = re.sub(
            rf"\b{expresion}\b",
            "",
            descripcion
        )

    # -------------------------------------------------
    # 3. Eliminar conectores de fecha/hora
    # -------------------------------------------------

    descripcion = re.sub(
        r"\ba\s+las\b",
        "",
        descripcion
    )

    descripcion = re.sub(
        r"\ba\s+la\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 4. Eliminar frases introductorias
    # -------------------------------------------------

    frases_introductorias = [
        "recuérdame",
        "recuerdame",
        "tengo una",
        "tengo un",
        "tengo"
    ]

    for frase in frases_introductorias:
        descripcion = descripcion.replace(frase, "")

    # -------------------------------------------------
    # 5. Limpiar espacios
    # -------------------------------------------------

    descripcion = re.sub(r"\s+", " ", descripcion).strip()

    # Eliminar "el" o "la" que hayan quedado
    # solos al final de la descripción.
    descripcion = re.sub(
        r"\s+(el|la)$",
        "",
        descripcion
    )

    return descripcion
def extract_description(text):
    """
    Extrae la descripción del evento
    eliminando las expresiones de fecha y hora.
    """

    descripcion = text.lower().strip()

    # -------------------------------------------------
    # 1. Eliminar expresiones completas de hora
    # -------------------------------------------------

    # Ejemplos:
    # a las 3 de la tarde
    # a las 8 de la mañana
    # a las 10 de la noche
    descripcion = re.sub(
        r"\ba\s+las\s+([1-9]|1[0-2])\s+de\s+la\s+(mañana|tarde|noche)\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 2. Eliminar horas con AM / PM
    # -------------------------------------------------

    # Ejemplos:
    # 5 am
    # 5 pm
    # 5 a.m.
    # 5 p.m.
    descripcion = re.sub(
        r"\b([1-9]|1[0-2])\s*(a\.?m\.?|p\.?m\.?)\.?",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 3. Eliminar horas en formato HH:MM
    # -------------------------------------------------

    # Ejemplos:
    # 10:30
    # 18:30
    # 8:00
    descripcion = re.sub(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 4. Eliminar mediodía y medianoche
    # -------------------------------------------------

    descripcion = re.sub(
        r"\b(al\s+)?mediodía\b",
        "",
        descripcion
    )

    descripcion = re.sub(
        r"\b(a\s+)?medianoche\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 5. Eliminar expresiones de fecha
    # -------------------------------------------------

    expresiones_fecha = [
        "pasado mañana",
        "mañana",
        "hoy",
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    for expresion in expresiones_fecha:
        descripcion = re.sub(
            rf"\b{expresion}\b",
            "",
            descripcion
        )

    # -------------------------------------------------
    # 6. Eliminar conectores de hora
    # -------------------------------------------------

    descripcion = re.sub(
        r"\ba\s+las\b",
        "",
        descripcion
    )

    descripcion = re.sub(
        r"\ba\s+la\b",
        "",
        descripcion
    )

    # -------------------------------------------------
    # 7. Eliminar frases introductorias
    # -------------------------------------------------

    frases_introductorias = [
        "recuérdame",
        "recuerdame",
        "tengo una",
        "tengo un",
        "tengo"
    ]

    for frase in frases_introductorias:
        descripcion = descripcion.replace(frase, "")

    # -------------------------------------------------
    # 8. Limpiar espacios
    # -------------------------------------------------

    descripcion = re.sub(r"\s+", " ", descripcion).strip()

    # Eliminar "el" o "la" que hayan quedado
    # solos al final de la descripción.
    descripcion = re.sub(
        r"\s+(el|la)$",
        "",
        descripcion
    )

    return descripcion

def parse_natural_language(text):
    """
    Analiza un mensaje en lenguaje natural.

    Detecta:
    - Fecha
    - Hora
    - Descripción

    Devuelve un datetime listo para Google Calendar.
    """

    fecha = detect_date(text)

    if fecha is None:
        return {
            "success": False,
            "error": "date_not_found"
        }

    hora = detect_time(text)

    if hora is None:
        return {
            "success": False,
            "error": "time_not_found"
        }

    if hora == "ambiguous":
        return {
            "success": False,
            "error": "ambiguous_time"
        }

    descripcion = extract_description(text)

    if not descripcion:
        return {
            "success": False,
            "error": "description_not_found"
        }

    hora_numero, minutos = hora

    start_datetime = datetime(
        fecha.year,
        fecha.month,
        fecha.day,
        hora_numero,
        minutos
    )

    return {
        "success": True,
        "start_datetime": start_datetime,
        "description": descripcion
    }