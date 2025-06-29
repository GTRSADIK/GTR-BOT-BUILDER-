
import requests
import json
import sqlite3
from flask import Flask, request

BOT_TOKEN = "7806603878:AAFa7ZC4IH3yHZcK3AoHtmu7H7gplIzHdjA"
ADMIN_ID = 7393768859

app = Flask(__name__)

# ✅ DB Setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS state (user_id INTEGER, step TEXT)")
conn.commit()

# ✅ Send Message
def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

# ✅ Edit Message
def edit_message(chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

# ✅ Store step
def set_user_step(user_id, step):
    cur.execute("DELETE FROM state WHERE user_id = ?", (user_id,))
    cur.execute("INSERT INTO state (user_id, step) VALUES (?, ?)", (user_id, step))
    conn.commit()

def get_user_step(user_id):
    cur.execute("SELECT step FROM state WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else None

# ✅ Start
def handle_start(message):
    u = message["from"]["id"]
    text = message.get("text", "")
    cur.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (u,))
    conn.commit()

    if text == "/admin":
        if u != ADMIN_ID:
            send_message(u, "⛔️ You are not authorized.")
            return
        msg = "👑 *Admin Panel*\n\nSelect an option below:"
        btn = {
            "inline_keyboard": [
                [{"text": "👥 All Users", "callback_data": "all_users"}],
                [{"text": "📢 Broadcast", "callback_data": "broadcast"}],
                [{"text": "🚫 Ban User", "callback_data": "ban_user"}],
                [{"text": "✅ Unban User", "callback_data": "unban_user"}]
            ]
        }
        send_message(u, msg, reply_markup=btn)
    else:
        msg = (
            "🎉 Hey Buddy Welcome To *GTR BOT BUILDER* 🤖\n\n"
            "🫶 *Thanks For Choosing Us* ❤️\n\n"
            "— Use The Bot Under Commands ⬇️"
        )
        btn = {
            "inline_keyboard": [
                [
                    {"text": "📊 Dashboard", "callback_data": "dashboard"},
                    {"text": "🛠 Create Bot", "callback_data": "create_bot"}
                ],
                [
                    {"text": "📋 My Bots", "callback_data": "my_bots"},
                    {"text": "ℹ️ Help", "callback_data": "help"}
                ]
            ]
        }
        send_message(u, msg, reply_markup=btn)

# ✅ Handle Callback
def handle_callback(call):
    u = call["from"]["id"]
    data = call["data"]
    msg_id = call["message"]["message_id"]

    if data == "create_bot":
        send_message(u, "✍️ Please send your *BotFather Token* to begin setup.")
        set_user_step(u, "awaiting_token")
    elif data == "dashboard":
        edit_message(u, msg_id, "📊 *Dashboard coming soon*", reply_markup=None)
    elif data == "start":
        handle_start({"from": {"id": u}, "text": "/start"})

# ✅ Handle Message for steps
def handle_user_message(message):
    u = message["from"]["id"]
    text = message.get("text", "")
    step = get_user_step(u)

    if step == "awaiting_token":
        if text.startswith("5") and ":" in text:
            # Very basic token check
            check = requests.get(f"https://api.telegram.org/bot{text}/getMe").json()
            if check.get("ok"):
                bot_name = check["result"]["first_name"]
                send_message(u, f"✅ Token Verified for *{bot_name}*.
🔧 Auto deployment coming soon!")
            else:
                send_message(u, "❌ Invalid Bot Token. Please try again.")
        else:
            send_message(u, "⚠️ Invalid format. Please send a valid token.")
        set_user_step(u, None)

# ✅ Webhook Endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        handle_user_message(update["message"])
        if update["message"].get("text", "").startswith("/start") or update["message"].get("text", "").startswith("/admin"):
            handle_start(update["message"])
    elif "callback_query" in update:
        handle_callback(update["callback_query"])
    return "ok", 200

# ✅ Run Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
