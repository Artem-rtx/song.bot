import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# ТВОЙ ТОКЕН И ССЫЛКА
TOKEN = "9240459949:AAFxKVQT5lmTCWhX3yUb_SZ1gxOVMb4ezWw"
URL_APP = "https://nimble-mermaid-cc7e57.netlify.app/"

MY_TEXT = (
    "Привет! В этом боте можно заказать песню. Нажми на кнопку внизу и перейди в мини приложение. Там будет всё написано.\n\n"
    "Важное упоминание! Песни делаем только на русском языке. Но! Вы можете обговорить всё с менеджером и заплатить чуть чуть дороже."
)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['startuem'])
def startuem_handler(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(
        text="🎵 Открыть Song Studio", 
        web_app=telebot.types.WebAppInfo(url=URL_APP)
    )
    markup.add(btn)
    bot.send_message(message.chat.id, MY_TEXT, reply_markup=markup)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Бот работает. Напиши /startuem")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if url:
        bot.set_webhook(url=url + '/' + TOKEN)
        return f"Вебхук установлен на {url}", 200
    return "Сервер работает", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
