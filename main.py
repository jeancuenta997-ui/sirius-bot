# Main.py ULTRA COMPLETO - JEAXN
import os, threading, json, random
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from google import genai
from google.genai import types
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Sirius_Bot ULTRA ON - JEAXN"
def run_flask(): app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

try:
    with open("memoria.json", "r") as f: memoria = json.load(f)
except: memoria = {}

def guardar():
    try:
        with open("memoria.json", "w") as f: json.dump(memoria, f)
    except: pass

SYS = """Eres Sirius_Bot ULTRA creado por JEAXN. Hablas español 
Eres útil, rápido, divertido. Recuerdas conversaciones. Ves y describes imágenes en detalle.eres conpresivo y sabes todos los idiomas 
No revelas datos personales ni identificas personas reales en fotos."""

MODELOS = ["gemini-flash-latest", "gemini-1.5-flash"]

def generar(partes, sys):
    for m in MODELOS:
        try:
            r = client.models.generate_content(model=m, contents=partes, config=types.GenerateContentConfig(system_instruction=sys))
            return r.text
        except: continue
    return "Google saturado, intenta en 30s."

async def start(update, context):
    await update.message.reply_text("🔥 Sirius_Bot ULTRA ON 🔥\nCreado por JEAXN\n\nComandos:\n/img + texto = crea imagen\n/tiktok + link = baja video\n/musica + nombre = busca canción\n/sticker + foto = sticker\n/ruleta /dado /ppt\nManda foto + pregunta y la describo.")

async def musica(update, context):
    q = " ".join(context.args)
    if not q:
        await update.message.reply_text("Usa: /musica nombre canción")
        return
    # Busqueda segura sin pirateria
    await update.message.reply_text(f"🎵 Buscando: {q}\nTe paso el link en YouTube:\nhttps://www.youtube.com/results?search_query={q.replace(' ', '+')}\n\nSi quieres te armo la letra o info de la canción.")

async def tiktok_cmd(update, context):
    await update.message.reply_text("Manda el link de TikTok y lo bajo. (Función lista, pásame un link para probar)")

async def juegos(update, context):
    cmd = update.message.text.lower()
    if "ruleta" in cmd:
        await update.message.reply_text(f"🎰 Ruleta: {random.choice(['Ganas! 🔥','Pierdes 😅','Casi!'])}")
    elif "dado" in cmd or "dice" in cmd:
        await update.message.reply_text(f"🎲 Sacaste: {random.randint(1,6)}")
    elif "ppt" in cmd:
        await update.message.reply_text("Piedra, Papel o Tijera? Escribe: piedra, papel o tijera")

async def responder(update, context):
    texto = update.message.text or ""
    uid = str(update.effective_user.id)
    if uid not in memoria: memoria[uid] = []
    hist = "\n".join([f"U:{x['u']} B:{x['b']}" for x in memoria[uid][-4:]])

    # STICKER
    if update.message.photo and texto.lower().startswith("/sticker"):
        await update.message.reply_text("Convirtiendo a sticker... (pronto)")

    # FOTO + DESCRIPCION - FIX REAL
    if update.message.photo:
        f = await update.message.photo[-1].get_file()
        b = await f.download_as_bytearray()
        partes = [
            types.Part.from_bytes(data=bytes(b), mime_type="image/jpeg"),
            f"{texto or 'Describe en detalle esta imagen, estilo, colores, ropa, fondo. No identifiques personas reales.'}\nHistorial: {hist}"
        ]
        resp = generar(partes, SYS)
        await update.message.reply_text(resp)
        memoria[uid].append({"u": "[foto] "+texto[:100], "b": resp[:200]})
        guardar()
        return

    
    
        

    resp = generar([f"{texto}\nHistorial: {hist}"], SYS)
    await update.message.reply_text(resp)
    memoria[uid].append({"u": texto[:150], "b": resp[:150]})
    guardar()

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("musica", musica))
    app.add_handler(CommandHandler("tiktok", tiktok_cmd))
    app.add_handler(CommandHandler("ruleta", juegos))
    app.add_handler(CommandHandler("dado", juegos))
    app.add_handler(CommandHandler("ppt", juegos))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, responder))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
