import telebot
import requests
from datetime import datetime
import random
from pprint import pprint
import wikipedia as wiki

wiki.set_lang("ru")
token = '1035021917:AAF-3Fki6dWOpQyyTqBbxoFQAEAwYz6fTlk'

bot = telebot.TeleBot(token)

states = {}
weather_states = {}


def weather_request(city='None', days=0):
    url = 'http://wttr.in/'

    if city == 'moon':
        url = url + 'moon' + '?QFT&lang=ru'
    elif city:
        url = url + city + '?' + str(days) + 'MQ'
    else:
        url = url + '?format=2'
    print('Sending weather request : ', url)
    ans = requests.get(url)
    return ans.text


def get_wiki(phrase):
    try:
        return wiki.summary(phrase)
    except:
        return "Запрос не найден"


@bot.message_handler(func=lambda message: True)  # states [message.from_user.id] == 'main'
def supervisor(message):
    user_id = message.from_user.id
    current_state = states.get(user_id, 'main')
    current_city = weather_states.get(user_id, '')
    print('Dictionary state in Supervisor :', weather_states)
    print('Current user : ', user_id, current_state)
    if current_state == 'main':
        main_handler(message)
    elif current_state == 'weather_date':
        weather_date_handler(message, current_city)
    elif current_state == 'moscow_weather':
        moscow_handler(message)


def main_handler(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Это бот-погода. Поможет узнать погоду в любом городе. Какой город интересует?'
                         )
    elif message.text.lower() in ('привет', 'hi', 'Hi!', 'привет!'):
        bot.reply_to(message, 'Привет, привет ' + message.from_user.first_name)

    elif message.text.lower() in ('погода на сегодня', 'погода', 'какая погода', 'weather',
                                  'what the weather', 'скажи погоду'):
        bot.send_message(message.chat.id, message.from_user.first_name + ' , а погода сейчас : ' + weather_request())
        bot.send_message(message.chat.id, message.from_user.first_name +
                         ' На сколько дней дать прогноз ( 1 / 2 / q ( выход')
        states[message.from_user.id] = 'weather_date'

    elif message.text.lower().startswith('москва'):
        bot.reply_to(message, 'Сейчас отличная погода! ' + weather_request('Москва'))

    elif message.text.lower().startswith('город '):
        print(message.text[5:])

        current_city = weather_states.get(message.from_user.id, message.text[6:])  # Writing City name to dictionary

        weather_states[message.from_user.id] = current_city

        print('Dictionary state (inside main handler ) :', weather_states, current_city)

        bot.send_message(message.chat.id, message.from_user.first_name
                         + ' , а погода сейчас в городе {}: '.format(message.text[:5].title()) +
                         weather_request(message.text[6:])
                         )
        bot.send_message(message.chat.id, message.from_user.first_name +
                         ' На сколько дней дать прогноз ( 1 / 2 / Выйти Q ?')
        states[message.from_user.id] = 'weather_date'

    elif message.text.lower() in ('луна', 'moon', 'покажи луну', 'show moon'):
        bot.reply_to(message, ' Все о луне что я знаю! ' + weather_request('moon'))

    elif message.text.lower() in ('погода завтра', 'погода на завтра', 'weather for tomorrow'):
        bot.reply_to(message, 'Завтра , будет: еще лучше !( Under construction)')

    elif message.text.lower().startswith('wiki '):
        ans = get_wiki(message.text[5:])
        bot.send_message(message.chat.id, ans)

    else:
        bot.send_message(message.chat.id, 'Я тебя не понял')


def moscow_handler(messasge):
    pass


def weather_date_handler(message, city):
    if message.text == '1':
        print('Handler for tomorrow done!')
        bot.send_message(message.from_user.id, ' Погода на завтра: ' + weather_request(city, days=1))
        states[message.from_user.id] = 'main'

    elif message.text == '2':
        bot.send_message(message.from_user.id, ' Прогноз на 2 дня: ' + weather_request(city, days=2))
        states[message.from_user.id] = 'main'

    elif message.text.lower() in ('q', 'exit', 'выход'):

        bot.send_message(message.from_user.id, ' Хорошего настроения ! ' + message.from_user.first_name)
        states[message.from_user.id] = 'main'
    else:
        bot.send_message(message.from_user.id, ' Не понял ... повторите ввод!')


bot.polling()
