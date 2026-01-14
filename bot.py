import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import secrets
import time

BOT_TOKEN = "8376026714:AAEND570PpBWc_ku915q7iZasL7JK8MKGco"  
REDIRECT_URL = "https://botbot-liard.vercel.app/"

bot = telebot.TeleBot(BOT_TOKEN)

REGISTERED_KEYS = [
    {
        "accessKey": "Cris-rank-2025",
        "name": "CrisUser",
        "subscription": "1 Day",
        "revoked": False,
        "expires": "2026-01-13",
        "telegram_id": 7634875658
    },
    {
        "accessKey": "Cris-rank-2026",
        "name": "CrisGame",
        "subscription": "💎 Premium",
        "revoked": False,
        "expires": "2099-01-14",
        "telegram_id": 6784382795
    }
]

TOKENS = {}

def get_user(tid):
    for u in REGISTERED_KEYS:
        if u["telegram_id"] == tid:
            return u
    return None

def is_expired(date_str):
    return datetime.now() > datetime.strptime(date_str, "%Y-%m-%d")

@bot.message_handler(commands=["start"])
def start(message):
    tid = message.chat.id
    user = get_user(tid)

    if not user:
        bot.send_message(
            tid,
            "❌ You are not registered yet.\n📩 Please contact the admin."
        )
        return

    if user["revoked"]:
        bot.send_message(tid, "🚫 Your access has been revoked.")
        return

    if is_expired(user["expires"]):
        bot.send_message(tid, "⏰ Your subscription has expired.")
        return

    
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {
        "telegram_id": tid,
        "expires": time.time() + 30
    }

    hidden_link = f"{REDIRECT_URL}?token={token}"

    text = (
    "👋 Welcome\n\n"
    f"👤 Username: {user['name']}\n"
    f"🆔 Telegram ID: {tid}\n"
    f"📦 Subscription: {user['subscription']}\n"
    f"🔐 Access Key: (click button below)\n"
)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔑 SHOW ACCESS KEY", callback_data="show_key")
    )
    kb.add(
        InlineKeyboardButton("🌐 OPEN WEB TOOL", url=hidden_link)
    )

    bot.send_message(tid, text, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == "show_key")
def show_key(call):
    tid = call.message.chat.id
    user = get_user(tid)

    if not user:
        bot.answer_callback_query(call.id, "Not registered", show_alert=True)
        return

    bot.answer_callback_query(
        call.id,
        f"🔐 ACCESS KEY:\n{user['accessKey']}",
        show_alert=True
    )

bot.remove_webhook()
bot.infinity_polling()
