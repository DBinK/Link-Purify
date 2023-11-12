import os
import telebot
import purify as pf
from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')

print("BOT_TOKEN：", BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "你好, 这里是链接净化Bot, 可以帮你把链接的跟踪参数清除, 甚至是诸如 B23.tv/XXXXX 的短链接")


@bot.message_handler(func=lambda msg: True)
def reply_purify_link(message):
    url = message.text
    clean_url = pf.remove_tracking_params_by_config(url, config)
    bot.reply_to(message, clean_url)


bot.infinity_polling()