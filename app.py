from flask import Flask, request, jsonify
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

from calendar_command import (
    process_agenda_command,
    process_natural_language_command
)

# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")  

print("===== CONFIGURACIÓN =====")
print("VERIFY_TOKEN:", bool(VERIFY_TOKEN))
print("WHATSAPP_TOKEN:", bool(WHATSAPP_TOKEN))
print("LONGITUD TOKEN:", len(WHATSAPP_TOKEN) if WHATSAPP_TOKEN else 0)
print("PHONE_NUMBER_ID:", PHONE_NUMBER_ID)


# ==========================================
# ENVIAR MENSAJE DE WHATSAPP
# ==========================================

def send_whatsapp_message(to, message):

    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("\n===== RESPUESTA DE META =====")
    print("Status code:", response.status_code)
    print("Respuesta:", response.text)

    return response


# ==========================================
# VERIFICACIÓN DEL WEBHOOK
# ==========================================


@app.route("/webhook", methods=["GET"])
def verify_webhook():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:

        print("✅ WEBHOOK VERIFICADO")

        return challenge, 200

    print("❌ ERROR EN VERIFICACIÓN DEL WEBHOOK")

    return "Token incorrecto", 403


# ==========================================
# RECIBIR MENSAJES DE WHATSAPP
# ==========================================


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    print("\n===== WEBHOOK RECIBIDO =====")
    print(data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        # ==========================================
        # IGNORAR ACTUALIZACIONES DE ESTADO
        # ==========================================

        if "statuses" in value:
            print("ℹ️ Actualización de estado de WhatsApp. Se ignora.")
            return jsonify({"status": "ok"}), 200

        # ==========================================
        # OBTENER MENSAJE
        # ==========================================

        if "messages" not in value:
            print("ℹ️ Webhook sin mensaje. Se ignora.")
            return jsonify({"status": "ok"}), 200

        message = value["messages"][0]

        sender = message["from"]

        print("\n===== USUARIO =====")
        print("Número:", sender)

        # ==========================================
        # COMPROBAR TIPO DE MENSAJE
        # ==========================================

        if message.get("type") != "text":

            send_whatsapp_message(
                sender,
                "⚠️ Por ahora solo puedo procesar mensajes de texto."
            )

            return jsonify({"status": "ok"}), 200

        # ==========================================
        # OBTENER TEXTO
        # ==========================================

        text = message["text"]["body"]

        print("Mensaje recibido:", text)

        # ==========================================
        # PROCESAR COMANDO
        # ==========================================

        if text.strip().lower() in ["ayuda", "help", "/ayuda"]:
            resultado = {
                "success": True,
                "message": (
                    "📅 *WhatsApp Calendar Bot*\n\n"
                    "Puedo ayudarte a crear eventos en Google Calendar.\n\n"
                    "📝 *Ejemplos:*\n\n"
                    "• Mañana a las 10:30 llevar el carro al taller\n"
                    "• El viernes a las 3 de la tarde tengo una reunión\n"
                    "• El sábado a las 8 de la noche ir a cenar\n"
                    "• Hoy a las 17:00 pagar la luz\n\n"
                    "📌 *También puedes usar el formato clásico:*\n\n"
                    "/agendar 20/09/2026 10:30 Llevar el carro al taller\n\n"
                    "💡 *Importante:*\n"
                    "Si escribes una hora como \"a las 5\", "
                    "especifica si es por la mañana, tarde o noche."
                )
            }

        elif text.strip().lower().startswith("/agendar"):
            resultado = process_agenda_command(text)

        else:
            resultado = process_natural_language_command(text)

        send_whatsapp_message(
            sender,
            resultado["message"]
        )

    except (KeyError, IndexError, TypeError) as error:

        print("⚠️ El webhook no contiene un mensaje válido.")
        print("Error:", error)

    return jsonify({"status": "ok"}), 200


@app.route("/test-calendar", methods=["GET"])
def test_calendar():
    from datetime import datetime, timedelta

    inicio = datetime.now() + timedelta(minutes=10)

    evento = create_calendar_event(
        title="Prueba desde Flask",
        start_datetime=inicio,
        description="Evento creado desde Flask.",
        duration_minutes=30
    )

    return jsonify({
        "status": "ok",
        "title": evento["summary"],
        "link": evento.get("htmlLink")
    })


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )