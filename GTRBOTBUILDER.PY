from flask import Flask, request
import requests, json

app = Flask(__name__)
BOT_TOKEN = "7806603878:AAFa7ZC4IH3yHZcK3AoHtmu7H7gplIzHdjA"

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup: payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def edit_message(chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup: payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def handle_start(message):
    u = message['from']['id']
    msg = (
        "🎉 Hey Buddy Welcome To *GTR BOT BUILDER* 🤖\n\n"
        "🫶 *Thanks For Choosing Us* ❤️\n"
        "— Use The Bot Under Commands ⬇️"
    )
    btn = {
        "inline_keyboard":[
            [
                {"text":"📊 Dashboard","callback_data":"dashboard"},
                {"text":"🛠 Create Bot","callback_data":"create_bot"}
            ],
            [
                {"text":"📋 My Bots","callback_data":"my_bots"},
                {"text":"ℹ️ Help","callback_data":"help"}
            ]
        ]
    }
    send_message(u, msg, btn)

def handle_callback(call):
    u = call['from']['id']; data = call['data']; msg_id = call['message']['message_id']
    if data=="dashboard":
        msg = (f"📊 *Dashboard Panel*\n\n👤 Name: {call['from']['first_name']}\n🆔 ID: `{u}`\n🤖 Total Bots: *2*")
        btn = {"inline_keyboard":[
            [{"text":"🛠 Create Bot","callback_data":"create_bot"},{"text":"📋 My Bots","callback_data":"my_bots"}],
            [{"text":"🔙 Back","callback_data":"start"}]
        ]}
        edit_message(u, msg_id, msg, btn)
    elif data=="create_bot":
        edit_message(u, msg_id, "🛠 *Send me your bot token now...*", None)
    elif data=="my_bots":
        msg = "📋 *Your Bots:*\n\n1. @MyFirstBot ✅\n2. @MySecondBot 🔄"
        btn = {"inline_keyboard":[[{"text":"🔙 Back","callback_data":"dashboard"}]]}
        edit_message(u, msg_id, msg, btn)
    elif data=="start":
        handle_start(call['message'])

@app.route('/webhook', methods=['POST'])
def webhook():
    upd = request.get_json()
    if 'message' in upd and upd['message'].get('text','')=='/start':
        handle_start(upd['message'])
    elif 'callback_query' in upd:
        handle_callback(upd['callback_query'])
    return "ok",200

if __name__ == '__main__':
    app.run(port=5000)
