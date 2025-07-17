import telebot
from handlers.convert import start_handler

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    start_handler(bot, message)

print("Бот працює...")
bot.polling(none_stop=True)
