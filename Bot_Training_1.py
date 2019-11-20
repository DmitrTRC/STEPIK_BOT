import telebot
import random
from pprint import pprint

token = '1035021917:AAF-3Fki6dWOpQyyTqBbxoFQAEAwYz6fTlk'

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Это БОТ пока он мало ,что умеет но активно учится :) В основном он синоптик! но поди знай ... '
                         )
    elif message.text in ('привет', 'Hi', 'hi', 'Hi!', 'Привет!', 'привет!'):
        bot.reply_to(message, 'Привет, привет ' + message.from_user.first_name)
    elif message.text == 'Погода на сегодня':
        bot.reply_to(message, 'Сегодня - сам в окно посмотри, не написал еще ...')

    else:
        bot.reply_to(message, 'Пока не понимаю , блин ...')


bot.polling()
