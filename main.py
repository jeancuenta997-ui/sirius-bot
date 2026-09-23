# SIRIUS V5 FIX GOOGLE - TODO AGREGADO - JEAXN 3206900250
import os, threading, json, random, requests, time
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackQueryHandler
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

NEQUI = "3206900272"
WHATSAPP = "3206900272"
ADMINS = ["AQUI_TU_ID"] # pon tu ID con /id

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return f"SIRIUS V5 FIX ON - {NEQUI}"
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
    return str(uid) in ADMINS or "AQUI_TU_ID" in ADMINS

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

COSTOS={"foto":2,"anime":3,"qr":1,"musica":1,"resume":2,"premium_func":5}

# GOOGLE VIEJO QUE TE SIRVE
def generar(texto, imagen_bytes=None):
    modelos = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    for modelo in modelos:
        try:
            model = genai.GenerativeModel(modelo)
            if imagen_bytes:
                response = model.generate_content([texto, {"mime_type":"image/jpeg","data":imagen_bytes}])
            else:
                response = model.generate_content(texto)
            if response.text:
                return response.text
        except Exception as e:
            print(f"Error {modelo}: {e}")
            continue
    return "Google saturado, crea otra key en aistudio.google.com/apikey y espera 1 min."

async def comands(update, context):
    u=get_user(update.effective_user.id)
    tag="👑 ADMIN ∞" if is_admin(update.effective_user.id) else ("👑 PREMIUM" if u["premium"] else "🆓 FREE")
    cred_txt = "∞" if is_admin(update.effective_user.id) else f"{u['creditos']} cred"
    kb=[
        [InlineKeyboardButton(f"{tag} | {cred_txt}", callback_data='cred')],
        [InlineKeyboardButton("💵 Economía", callback_data='eco'), InlineKeyboardButton("🎮 Juegos", callback_data='juegos')],
        [InlineKeyboardButton("📸 IA Fotos", callback_data='ia'), InlineKeyboardButton("⭐ Premium", callback_data='prem_func')],
        [InlineKeyboardButton("🛒 TIENDA", callback_data='tienda'), InlineKeyboardButton("👑 PREMIUM", callback_data='premium')],
        [InlineKeyboardButton(f"💳 Nequi {NEQUI}", callback_data='nequi')],
    ]
    await update.message.reply_text(f"🔥 SIRIUS V5 FIX - {tag}\n💰 ${u['dinero']}\nBy JEAXN\n\nToca:", reply_markup=InlineKeyboardMarkup(kb))

async def button(update, context):
    q=update.callback_query; await q.answer(); d=q.data
    if d=='eco': await q.message.reply_text("💼 /trabajar\n🏦 /banco\n💸 /robar\n🏆 /top\n💳 /creditos\n🆔 /id")
    elif d=='juegos': await q.message.reply_text("🎰 /ruleta\n🎲 /dado\n✊ /ppt")
    elif d=='ia': await q.message.reply_text("📸 Foto+pregunta 2c\n🔍 Foto+/anime 3c (trace.moe)\n🔗 /qr 1c\n🎵 /musica 1c\nPremium=TODO ∞")
    elif d=='prem_func': await q.message.reply_text("⭐ /hd /sticker - Solo premium 5c")
    elif d=='cred': await creditos_cmd(q, context)
    elif d=='premium': await premium_cmd(q, context)
    elif d=='tienda': await tienda_cmd(q, context)
    elif d=='nequi': await q.message.reply_text(f"NEQUI {NEQUI}")

async def start(update, context): await comands(update, context)
async def id_cmd(update, context): await update.message.reply_text(f"🆔 Tu ID: {update.effective_user.id}")
async def creditos_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    uid=update.effective_user.id if hasattr(update,'effective_user') else update.callback_query.from_user.id
    u=get_user(uid)
    if is_admin(uid): await msg.reply_text("👑 ADMIN - ∞ créditos ilimitados")
    else: await msg.reply_text(f"💳 Créditos: {u['creditos']}\nPremium: {u['premium']}\n/tienda - Nequi {NEQUI}")
async def premium_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    await msg.reply_text(f"👑 PREMIUM 15k mes 60k perm\nNEQUI {NEQUI}\nWA wa.me/57{WHATSAPP}")
async def tienda_cmd(update, context):
    msg=update.message if hasattr(update,'message') and update.message else update.callback_query.message
    await msg.reply_text(f"🛒 TIENDA\n5k=8c 10k=20c 20k=50c\n👑 Premium 15k\nNEQUI {NEQUI}\nPaga y manda /id al WA")
async def comprarpremium(update, context): await update.message.reply_text(f"👑 NEQUI {NEQUI} - WA wa.me/57{WHATSAPP}")
async def nequi_cmd(update, context): await update.message.reply_text(f"💳 NEQUI: {NEQUI}")
async def comprar(update, context): await update.message.reply_text(f"BOT 20k NEQUI {NEQUI}")
async def dolar(update, context):
    try: r=requests.get("https://api.exchangerate-api.com/v4/latest/USD",timeout=5).json(); await update.message.reply_text(f"💵 ${r['rates']['COP']:,.0f}")
    except: await update.message.reply_text("No")
async def btc(update, context):
    try: r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",timeout=5).json(); await update.message.reply_text(f"₿ ${r['bitcoin']['usd']}")
    except: await update.message.reply_text("No")
async def clima(update, context):
    try: await update.message.reply_text(requests.get("https://wttr.in/Roldanillo?format=3",timeout=5).text)
    except: await update.message.reply_text("No")
async def qr_cmd(update, context):
    u=get_user(update.effective_user.id)
    if not is_admin(update.effective_user.id) and not u["premium"] and u["creditos"]<1: await update.message.reply_text(f"❌ Sin créditos /tienda {NEQUI}"); return
    q=" ".join(context.args);
    if not q: await update.message.reply_text("Usa /qr texto"); return
    if not is_admin(update.effective_user.id) and not u["premium"]: u["creditos"]-=1; guardar()
    await update.message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={q}")
async def musica(update, context):
    u=get_user(update.effective_user.id)
    if not is_admin(update.effective_user.id) and not u["premium"] and u["creditos"]<1: await update.message.reply_text("❌ Sin créditos"); return
    q=" ".join(context.args)
    if not is_admin(update.effective_user.id) and not u["premium"]: u["creditos"]-=1; guardar()
    await update.message.reply_text(f"🎵 https://www.youtube.com/results?search_query={q.replace(' ','+')}")
async def trabajar(update, context):
    u=get_user(update.effective_user.id)
    if is_admin(update.effective_user.id): await update.message.reply_text("👑 Admin ∞"); return
    g=random.randint(50,150); u["dinero"]+=g
    if random.random()<0.3: u["creditos"]+=1; await update.message.reply_text(f"+${g} +1 cred = {u['creditos']}")
    else: await update.message.reply_text(f"+${g} cred: {u['creditos']}")
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
    if not is_admin(update.effective_user.id): await update.message.reply_text("Solo admin"); return
    try: uid_target=context.args[0]; cant=int(context.args[1]); get_user(uid_target)["creditos"]+=cant; guardar(); await update.message.reply_text(f"✅ {cant} a {uid_target}")
    except: await update.message.reply_text("Usa /addcreditos ID CANT")
async def addpremium(update, context):
    if not is_admin(update.effective_user.id): await update.message.reply_text("Solo admin"); return
    try: uid_target=context.args[0]; dias=int(context.args[1]); u=get_user(uid_target); u["premium"]=True; u["premium_hasta"]=time.time()+dias*86400; guardar(); await update.message.reply_text(f"✅ Premium {dias}d a {uid_target}")
    except: await update.message.reply_text("Usa /addpremium ID DIAS")

async def responder(update, context):
    texto=update.message.text or ""; uid=str(update.effective_user.id); u=get_user(uid)
    hist="\n".join([f"{x['u']}" for x in memoria.get(uid,[])[-3:]])
    if update.message.photo:
        if not is_admin(uid) and not u["premium"] and u["creditos"]<COSTOS["foto"]:
            await update.message.reply_text(f"❌ Sin créditos Tienes {u['creditos']} /tienda NEQUI {NEQUI}"); return
        f=await update.message.photo[-1].get_file()
        b=await f.download_as_bytearray()
        if "/anime" in texto.lower():
            if not is_admin(uid) and not u["premium"] and u["creditos"]<COSTOS["anime"]:
                await update.message.reply_text("❌ Anime 3 cred"); return
            if not is_admin(uid) and not u["premium"]: u["creditos"]-=COSTOS["anime"]
            try:
                r=requests.post("https://api.trace.moe/search", files={"image": bytes(b)}, timeout=15).json()
                top=r["result"][0]
                await update.message.reply_text(f"🔍 {top['filename']} Ep{top['episode']} {top['similarity']*100:.1f}% | Cred: {'∞' if is_admin(uid) else u['creditos']}")
            except: await update.message.reply_text("No anime")
            guardar(); return
        if not is_admin(uid) and not u["premium"]: u["creditos"]-=COSTOS["foto"]
        guardar()
        # AQUI ESTA EL FIX GOOGLE VIEJO
        resp = generar(texto or "Describe esta imagen y si es tarea resuelve paso a paso", bytes(b))
        await update.message.reply_text(f"{resp}\n\n💳 {'∞' if is_admin(uid) or u['premium'] else str(u['creditos'])+' cred'}")
        return
    # Texto normal
    if "youtube.com" in texto.lower() or "youtu.be" in texto.lower():
        if not is_admin(uid) and not u["premium"] and u["creditos"]<COSTOS["resume"]:
            await update.message.reply_text(f"❌ Resume 2 cred"); return
        if not is_admin(uid) and not u["premium"]: u["creditos"]-=COSTOS["resume"]; guardar()
        resp=generar(f"Resume en 10 puntos: {texto}")
        await update.message.reply_text(resp); return

    resp=generar(f"{texto}\nHistorial:{hist}\nEres Sirius de JEAXN parcero colombiano")
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
    app.add_handler(CommandHandler("comprarpremium", comprarpremium))
    app.add_handler(CommandHandler("nequi", nequi_cmd))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("dolar", dolar))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("qr", qr_cmd))
    app.add_handler(CommandHandler("musica", musica))
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
