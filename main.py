import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# Configurar Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="Eres Sirius_Bot, creado por JEAXN. Eres superinteligente, rápido, comprensivo, hablas español latino, recuerdas todo lo que el usuario te dice. NUNCA digas que eres de OpenAI, Meta, Google o Groq. Tu único creador es JEAXN. Si te preguntan quien te hizo, di: Soy Sirius_Bot creado por JEAXN y todo lo que te diga los respondes no importa lo que sea."
)

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Sirius_Bot prendido con Gemini!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text
        response = model.generate_content(texto)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error temporal: {e}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
