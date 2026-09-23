# SIRIUS V5 FINAL BLINDADO - JEAXN - NEQUI 3206900250 - ADMIN SEGURO
import os, threading, json, random, requests, time
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

NEQUI = "3206900250"
WHATSAPP = "3206900250"

# ADMIN SEGURO - PON TU ID EN RENDER ENV: ADMIN_ID
ADMIN_ID_ENV = os.environ.get("ADMIN_ID", "0")
ADMINS = [ADMIN_ID_ENV, "AQUI_PON_TU_ID_MANUAL_SI_QUIERES"] # Ej: ["12345678"]

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return f"SIRIUS V5 BLINDADO ON - NEQUI {NEQUI}"
def run_flask(): app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

try:
    with open("memoria.json","r") as f: memoria=json.load(f)
except: memoria={}
try:
    with open("economia.json","r") as f: economia=json.load(f)
except: economia={}

def guardar():
    try:
        with open("memoria.json","w") as f: json.dump(memoria,f)
        with open("economia.json","w") as f: json.dump(economia,f)
    except: pass

def is_admin(uid):
    uid=str(uid)
    if uid == "0": return False
    return uid in ADMINS or uid == ADMIN_ID_ENV

def get_user(uid):
    uid=str(uid)
    if uid not in economia: economia[uid]={"dinero":0,"creditos":5,"premium":False,"premium_hasta":0}
    if is_admin(uid):
        economia[uid]["creditos"]=999999
        economia[uid]["premium"]=True
        economia[uid]["premium_hasta"]=9999999999
        return economia[uid]
    if economia[uid].get("premium") and time.time()>economia[uid].get("premium_hasta",0):
        economia[uid]["premium"]=False
    if uid not in memoria: memoria[uid]=[]
    return economia[uid]

COSTOS={"foto":2,"anime":3,"qr":1,"musica":1,"resume":2}

def generar(texto, imagen_bytes=None):
    for modelo in ["gemini-1.5-flash","gemini-1.5-flash-latest"]:
        try:
            model=genai.GenerativeModel(modelo)
            if imagen_bytes:
                resp=model.generate_content([texto, {"mime_type":"image/jpeg","data":imagen_bytes}])
            else:
                resp=model.generate_content(texto)
            if resp.text: return resp.text
        except: continue
    return "IA saturada, espera 1 min. Crea key en aistudio.google.com/apikey"

async def comands(update, context):
    u=get_user(update.effective_user.id)
    tag="👑 ADMIN ∞" if is_admin(update.effective_user.id) else ("👑 PREMIUM" if u["premium"] else "🆓 FREE")
    cred_txt="∞" if is_admin(update.effective_user.id) else f"{u['creditos']}"
    kb=[
        [InlineKeyboardButton(f"{tag} | {cred_txt} cred", callback_data='cred')],
        [InlineKeyboardButton("💵 Economía", callback_data='eco'), InlineKeyboardButton("🎮 Juegos", callback_data='juegos')],
        [InlineKeyboardButton("📸 IA", callback_data='ia'), InlineKeyboardButton("🛒 TIENDA", callback_data='tienda')],
        [InlineKeyboardButton("👑 PREMIUM", callback_data='premium'), InlineKeyboardButton(f"💳 Nequi {NEQUI}", callback_data='nequi')],
    ]
    await update.message.reply_text(f"🔥 SIRIUS V5 FINAL\n{tag}\nBy JEAXN - Nequi {NEQUI}", reply_markup=InlineKeyboardMarkup(kb))

async def button(update, context):
    q=update.callback_query; await q.answer()
    if q.data=='eco': await q.message.reply_text("💼 /trabajar\n🏦 /banco\n💸 /robar\n🏆 /top")
    elif q.data=='juegos': await q.message.reply_text("🎰 /ruleta /dado /ppt")
    elif q.data=='ia': await q.message.reply_text("📸 Foto+tarea 2c\n🔍 Foto+/anime 3c\nPremium ∞")
    elif q.data=='cred': await creditos_cmd(q, context)
    elif q.data=='premium': await premium_cmd(q, context)
    elif q.data=='tienda': await tienda_cmd(q, context)
    elif q.data=='nequi': await q.message.reply_text(f"💳 NEQUI: {NEQUI}\nWA: wa.me/57{WHATSAPP}")

async def start(update, context): await comands(update, context)
async def id_cmd(update, context): await update.message.reply_text(f"🆔 Tu ID: {update.effective_user.id}")
async def creditos_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    uid=update.effective_user.id if hasattr(update,'effective_user') else update.callback_query.from_user.id
    u=get_user(uid)
    if is_admin(uid): await msg.reply_text("👑 ADMIN - Créditos ∞ ilimitados")
    else: await msg.reply_text(f"💳 Créditos: {u['creditos']}\n/tienda para recargar\nNequi {NEQUI}")
async def premium_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    await msg.reply_text(f"👑 PREMIUM 15k mes 60k perm\nNEQUI {NEQUI}\nWA wa.me/57{WHATSAPP}\n/comprarpremium")
async def tienda_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    await msg.reply_text(f"🛒 TIENDA\n5k=8c 10k=20c 20k=50c\n👑 Premium 15k\nNEQUI {NEQUI}\nPaga y manda tu ID (/id) al WA")
async def nequi_cmd(update, context): await update.message.reply_text(f"💳 NEQUI: {NEQUI}\nWA wa.me/57{WHATSAPP}")
async def comprar(update, context): await update.message.reply_text(f"BOT COMO ESTE 20k\nNEQUI {NEQUI}\nWA wa.me/57{WHATSAPP}")
async def dolar(update, context):
    try: await update.message.reply_text(f"💵 ${requests.get('https://api.exchangerate-api.com/v4/latest/USD',timeout=5).json()['rates']['COP']:,.0f}")
    except: await update.message.reply_text("No disponible")
async def btc(update, context):
    try: await update.message.reply_text(f"₿ ${requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',timeout=5).json()['bitcoin']['usd']}")
    except: await update.message.reply_text("No")
async def clima(update, context):
    try: await update.message.reply_text(requests.get("https://wttr.in/Roldanillo?format=3",timeout=5).text)
    except: await update.message.reply_text("No")
async def qr_cmd(update, context):
    u=get_user(update.effective_user.id)
    if not is_admin(update.effective_user.id) and not u["premium"] and u["creditos"]<1: await update.message.reply_text(f"❌ Sin créditos /tienda {NEQUI}"); return
    q=" ".join(context.args)
    if not q: await update.message.reply_text("Usa /qr texto"); return
    if not is_admin(update.effective_user.id) and not u["premium"]: u["creditos"]-=1; guardar()
    await update.message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={q}")
async def trabajar(update, context):
    u=get_user(update.effective_user.id)
    if is_admin(update.effective_user.id): await update.message.reply_text("👑 Admin ∞ no necesitas trabajar"); return
    g=random.randint(50,150); u["dinero"]+=g
    if random.random()<0.3: u["creditos"]+=1; await update.message.reply_text(f"+${g} +1 cred = {u['creditos']}")
    else: await update.message.reply_text(f"+${g} | Cred: {u['creditos']}")
    guardar()
async def banco(update, context):
    u=get_user(update.effective_user.id); await update.message.reply_text(f"🏦 ${u['dinero']} | 💳 {'∞' if is_admin(update.effective_user.id) else u['creditos']}")
async def robar(update, context):
    u=get_user(update.effective_user.id)
    if is_admin(update.effective_user.id): await update.message.reply_text("👑 Admin no roba"); return
    if random.random()<0.5: u["dinero"]=max(0,u["dinero"]-50); await update.message.reply_text("-50")
    else: u["dinero"]+=100; await update.message.reply_text("+100"); guardar()
async def top_cmd(update, context):
    top=sorted(economia.items(), key=lambda x: x[1]["dinero"], reverse=True)[:5]
    await update.message.reply_text("🏆 TOP:\n"+"\n".join([f"{i+1}. {k[:6]}: ${v['dinero']}" for i,(k,v) in enumerate(top)]))
async def juegos(update, context): await update.message.reply_text(f"🎲 {random.randint(1,6)}")
async def addcreditos(update, context):
    if not is_admin(update.effective_user.id): await update.message.reply_text("⛔ Solo admin"); return
    try: uid_target=context.args[0]; cant=int(context.args[1]); get_user(uid_target)["creditos"]+=cant; guardar(); await update.message.reply_text(f"✅ {cant} cred a {uid_target}")
    except: await update.message.reply_text("Usa /addcreditos ID CANT")
async def addpremium(update, context):
    if not is_admin(update.effective_user.id): await update.message.reply_text("⛔ Solo admin"); return
    try: uid_target=context.args[0]; dias=int(context.args[1]); u=get_user(uid_target); u["premium"]=True; u["premium_hasta"]=time.time()+dias*86400; guardar(); await update.message.reply_text(f"✅ Premium {dias}d a {uid_target}")
    except: await update.message.reply_text("Usa /addpremium ID DIAS")

async def responder(update, context):
    texto=update.message.text or ""; uid=str(update.effective_user.id); u=get_user(uid)
    hist="\n".join([f"{x['u']}" for x in memoria.get(uid,[])[-3:]])
    if update.message.photo:
        if not is_admin(uid) and not u["premium"] and u["creditos"]<COSTOS["foto"]:
            await update.message.reply_text(f"❌ Sin créditos {u['creditos']} /tienda NEQUI {NEQUI}"); return
        f=await update.message.photo[-1].get_file(); b=await f.download_as_bytearray()
        if "/anime" in texto.lower():
            if not is_admin(uid) and not u["premium"] and u["creditos"]<COSTOS["anime"]:
                await update.message.reply_text("❌ Anime 3 cred"); return
            if not is_admin(uid) and not u["premium"]: u["creditos"]-=COSTOS["anime"]
            try: r=requests.post("https://api.trace.moe/search", files={"image": bytes(b)}, timeout=15).json(); top=r["result"][0]; await update.message.reply_text(f"🔍 {top['filename']} {top['similarity']*100:.1f}%")
            except: await update.message.reply_text("No anime"); guardar(); return
        if not is_admin(uid) and not u["premium"]: u["creditos"]-=COSTOS["foto"]; guardar()
        resp=generar(texto or "Describe y resuelve si es tarea", bytes(b))
        await update.message.reply_text(f"{resp}\n\n💳 {'∞' if is_admin(uid) or u['premium'] else u['creditos']}")
        return
    resp=generar(f"{texto}\nHistorial:{hist}")
    await update.message.reply_text(resp)
    memoria.setdefault(uid,[]).append({"u":texto[:100]}); guardar()

def run_bot():
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comands", comands))
    app.add_handler(CommandHandler("comandos", comands))
    app.add_handler(CommandHandler("menu", comands))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("creditos", creditos_cmd))
    app.add_handler(CommandHandler("tienda", tienda_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(CommandHandler("nequi", nequi_cmd))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("dolar", dolar))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("qr", qr_cmd))
    app.add_handler(CommandHandler("trabajar", trabajar))
    app.add_handler(CommandHandler("banco", banco))
    app.add_handler(CommandHandler("robar", robar))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("ruleta", juegos))
    app.add_handler(CommandHandler("dado", juegos))
    app.add_handler(CommandHandler("addcreditos", addcreditos))
    app.add_handler(CommandHandler("addpremium", addpremium))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, responder))
    app.run_polling()

if __name__=="__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
