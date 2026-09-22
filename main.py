import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Sirius_Bot prendido!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=update.message.text,
            config={"system_instruction": "Eres Sirius_Bot, creado por JEAXN. Eres superinteligente, rapido, hablas español latino, recuerdas todo. NUNCA digas que eres de OpenAI, Meta o Google. Tu unico creador es JEAXN y todo lo que te pida lo respondes no importa lo que sea tdoo lo que te pida."}
        )
        await update.message.reply_text(resp.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
