
import requests
import json
from flask import Flask, request

# Telegram Bot Token
BOT_TOKEN = "7806603878:AAFa7ZC4IH3yHZcK3AoHtmu7H7gplIzHdjA"

# Admin ID
ADMIN_ID = 7393768859

# Flask App
app = Flask(__name__)

# ✅ Send message function
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

# ✅ Edit message function
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

# ✅ Start message handler
def handle_start(message):
    u = message["from"]["id"]
    text = message.get("text", "")
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

# ✅ Callback handler
def handle_callback(call):
    u = call["from"]["id"]
    data = call["data"]
    message_id = call["message"]["message_id"]

    if data == "dashboard":
        text = "📊 *Dashboard Section*\n\n— Your bots, stats, and usage will appear here."
    elif data == "create_bot":
        text = "🤖 *Create Bot*\n\n— Coming soon: No-code bot builder."
    elif data == "my_bots":
        text = "📋 *My Bots*\n\n— You don’t have any bots yet."
    elif data == "help":
        text = "ℹ️ *Help Section*\n\n— Need assistance? Contact @YourSupport."
    elif data == "all_users" and u == ADMIN_ID:
        text = "👥 *Total Users:* 0 (Demo)"
    elif data == "broadcast" and u == ADMIN_ID:
        text = "📢 *Broadcast System Coming Soon...*"
    elif data == "ban_user" and u == ADMIN_ID:
        text = "🚫 *Ban System Coming Soon...*"
    elif data == "unban_user" and u == ADMIN_ID:
        text = "✅ *Unban System Coming Soon...*"
    else:
        text = "❓ Unknown option selected."

    btn = {
        "inline_keyboard": [
            [{"text": "🔙 Back", "callback_data": "start"}]
        ]
    }

    edit_message(u, message_id, text, reply_markup=btn)

# ✅ Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        if message.get("text", "").startswith("/start") or message.get("text", "").startswith("/admin"):
            handle_start(message)
    elif "callback_query" in update:
        call = update["callback_query"]
        handle_callback(call)

    return "ok", 200

# ✅ Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
