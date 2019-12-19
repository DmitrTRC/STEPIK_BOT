import telebot
import re
import datetime
import requests
from weatherapi import *
from Dispatcher import *
from aux_data import *  # Telegram API KEY, GEO API, , Weather API , extra data
from datetime import date, timedelta

bot = telebot.TeleBot(bot_token)
info_weather = CWeatherInfo()

calls = {}  # User statistics
current_shown_dates = {}  # Selected dates

task = CDispatcher({

})  # Menu task handler@bot.message_handler(func=lambda message: True)


def pares_date(date_str):
    ret_str = filter(None, re.split("[, /.\-!?:]+", date_str))
    day, month = map(int, ret_str)
    return day, month


@bot.message_handler(commands=['start'])
def frontier_handler(message):
    print(f'Write frontier handling starting... {message.from_user.id}')
    if message.from_user.id not in calls:  # Set to 0 User statistics if not found in calls
        calls[message.from_user.id] = 0
        bot.send_message(message.chat.id, 'Это бот-погода. Поможет узнать погоду в любом городе. /info - помощь ')
    else:
        calls[message.from_user.id] += 1
        today = date.today()
        # cur_date = (today.year, today.month, today.day)
        current_shown_dates[message.from_user.id] = today
        bot.send_message(message.chat.id, 'Введите город и дату в предела 3 суток.')


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_message(message.from_user.id, GREETING_MSG)


@bot.message_handler(commands=['moon'])
def moon_handler(message):
    url_moon = 'http://wttr.in/moon'
    bot.send_message(message.from_user.id,
                     requests.get(url_moon, params={'QFT': '', 'lang': 'ru'}).text)


@bot.message_handler(commands=['weather'])
def weather(message):
    report = info_weather.get_detailed_report(info_weather.get_weather(LOCATION.city))
    base_text = f'Температура на сегодня в городе {LOCATION.city.capitalize()} {round(report[0])} {degree_sign}C;\n'
    if not report[1]:
        msg_text = base_text + f'Скорость ветра {report[2]} м/с;\n {report[3]}.'
    else:
        msg_text = base_text + f'{report[1]}, {report[2]} м/с;\n {report[3]}.'

    bot.send_message(message.from_user.id, msg_text)


@bot.message_handler(commands=['calls'])
def calls_handle(message):
    bot.send_message(message.from_user.id,
                     message.from_user.first_name + ' ' + str(calls.get(message.from_user.id)))


@bot.message_handler(content_types=['text'])
def weather_parser(message):
    today = date.today()
    msg_string = message.text.lower().split()
    if len(msg_string) == 1:
        print('weather requests', msg_string[0])
    elif len(msg_string) == 2:
        try:
            day, month = pares_date(msg_string[1])
        except ValueError:
            bot.send_message(message.from_user.id, 'Неправильный формат даты ... ')
        else:
            try:
                req_date = date(today.year, month, day)
            except ValueError:
                bot.send_message(message.from_user.id, 'Неправильный формат даты ... ')
            else:
                dif = req_date - today
                if 3 < dif.days or dif.days < 0:
                    bot.send_message(message.from_user.id, 'Неправильный формат даты ( в пределах 3-х суток )')
                else:
                    current_shown_dates[message.from_user.id] = req_date  # Selected dates
                    print('Weather request ', msg_string[0], req_date)
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понял !!!')


if __name__ == '__main__':
    # bot.skip_pending = True
    bot.polling(none_stop=True)
