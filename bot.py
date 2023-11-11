import os
import telebot
import purify as pf

BOT_TOKEN = os.environ.get('BOT_TOKEN')


print("BOT_TOKEN：", BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def reply_purify_link(message):
    url = message.text
    clean_url = pf.remove_tracking_params_by_config(url, config)
    bot.reply_to(message, clean_url)


bot.infinity_polling()