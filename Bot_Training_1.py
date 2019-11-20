import telebot
import random

token = '1035021917:AAF-3Fki6dWOpQyyTqBbxoFQAEAwYz6fTlk'

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text == '/start':
        bot.reply_to(message,
                     'Это БОТ пока он мало ,что умеет но активно учится :) В основном он синоптик! но поди знай ... ')
    elif message.text in ('привет', 'Hi', 'hi', 'Hi!', 'Привет!', 'привет!'):
        bot.reply_to(message, 'Привет, привет')
    elif message.text == 'Погода на сегодня':
        bot.reply_to(message, 'Сегодня - сам в окно посмотри, не написал еще ...')


bot.polling()
