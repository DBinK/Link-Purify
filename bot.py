import os
import telebot
from telebot import types
import purify
from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')

print("BOT_TOKEN: ", BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "你好, 这里是链接净化Bot, 可以帮你把链接的跟踪参数清除, 甚至是诸如 B23.tv/XXXXX 的短链接")


@bot.message_handler(func=lambda msg: True)
def reply_purify_link(message):
    text = message.text
    clean_url = purify.process_url(text)
    bot.reply_to(message, clean_url)

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    text = inline_query.query
    try:
        clean_url = purify.process_url(text)
        r = types.InlineQueryResultArticle('1', '只有净化后的链接', types.InputTextMessageContent(clean_url))
        r2 = types.InlineQueryResultArticle('2', '原始文字和净化后的链接', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
'''
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)'''

bot.infinity_polling()