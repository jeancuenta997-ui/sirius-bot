import os, threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
client = Groq(api_key=GROQ_KEY)

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Sirius_Bot prendido!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

SYSTEM = "Eres Sirius_Bot, super inteligente, rapido, comprensivo, hablas español latino, recuerdas todo, creado por JEAXN."

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": update.message.text}],
        max_tokens=1000
    )
    await update.message.reply_text(completion.choices[0].message.content)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
