from datetime import datetime
import requests
from telegram import Bot

import os
from datetime import datetime
import requests
from telegram import Bot

# ✅ Configura tus datos desde variables de entorno
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL_RECORDATORIOS = os.environ["URL_RECORDATORIOS"]

# 🟢 Configura tus datos aquí
#TOKEN = "7408806495:AAGzphvP6LZfCjVjzMKaZsuErKdaz9Ojwac"
#CHAT_ID = -1002800656521  # puede ser ID de grupo o canal
#URL_RECORDATORIOS = "https://api.sheetbest.com/sheets/8464ab9b-9fda-467a-a722-ad469e3cf4d8"

# 🧠 Inicializa el bot
bot = Bot(token=TOKEN)

def notificar_eventos_hoy():
    hoy = datetime.now().strftime("%Y-%m-%d")
    try:
        response = requests.get(URL_RECORDATORIOS)
        data = response.json()
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al consultar los recordatorios.")
        return

    cumple_hoy = []
    eventos_hoy = []

    for item in data:
        if item["fecha"] == hoy:
            if item["tipo"].lower() == "cumpleaños":
                cumple_hoy.append(f"🎂 ¡Hoy es el Onomastico de *{item['nombre']}*! 🎉")
            elif item["tipo"].lower() == "evento":
                eventos_hoy.append(f"📌 *{item['nombre']}*\n🕒 {item.get('hora', '') or ''} 📍 {item.get('ubicacion', '') or ''}")

    if cumple_hoy or eventos_hoy:
        mensaje = "🎊 *Recordatorio de hoy* 🎊\n\n"
        if cumple_hoy:
            mensaje += "\n".join(cumple_hoy) + "\n\n"
        if eventos_hoy:
            mensaje += "\n".join(eventos_hoy)

        bot.send_message(chat_id=CHAT_ID, text=mensaje.strip(), parse_mode="Markdown")
    else:
        print("✅ No hay Onomasticos ni eventos hoy.")

# 📢 Ejecutar
notificar_eventos_hoy()
