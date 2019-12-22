import telebot
import re
import datetime
from weatherapi import *
from aux_data import *  # Telegram API KEY, GEO API, , Weather API , extra data
from datetime import date, timedelta
import wikipedia as wiki
from telebot import types
import logging

logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                              '%m-%d %H:%M:%S')
ch = logging.FileHandler('LOG.txt')
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)

bot = telebot.TeleBot(bot_token)

info_weather = CWeatherInfo()
CURRENT_CITY = None
user_defined = {
    # User settings
}
wiki.set_lang("ru")

calls = {}  # User statistics
current_shown_dates = {}  # Selected dates


def pares_date(date_str):
    ret_str = filter(None, re.split("[, /.\-!?:]+", date_str))
    day, month = map(int, ret_str)
    return day, month


@bot.message_handler(commands=['start'])
def frontier_handler(message):
    print(
        f'Write frontier handling starting... {message.from_user.id} {message.from_user.first_name}')  # Debug information
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('/Moscow')
    button2 = types.KeyboardButton('/info')
    button3 = types.KeyboardButton('/wiki')
    button4 = types.KeyboardButton('/calls')

    markup.add(button1, button2)
    markup.add(button3, button4)

    if message.from_user.id not in calls:  # Set to 0 User statistics if not found in calls
        calls[message.from_user.id] = {
            'wiki': 0,
            'weather': 0,
            'moon': 0,
        }
        bot.send_message(message.chat.id, 'Это бот-погода. Поможет узнать погоду в любом городе. /info - помощь ',
                         reply_markup=markup)
    else:

        today = date.today()
        current_shown_dates[message.from_user.id] = today
        bot.send_message(message.chat.id,
                         'Введите город и дату (дд,мм) в пределах 3 суток. Или может Вы дадите другую комманду ?',
                         reply_markup=markup)


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_message(message.from_user.id, GREETING_MSG)


@bot.message_handler(commands=['wiki'])
def wiki_handler(message):
    try:
        calls[message.from_user.id]['wiki'] += 1
    except KeyError:
        print('User identification error in wiki')

    bot.send_message(message.from_user.id, 'Ок! Я - Wiki Напиши мне свой запрос ...')
    bot.register_next_step_handler(message, wiki_response)


def wiki_response(message):
    try:
        answer = wiki.summary(message.text)
    except Exception:
        print('Not Found')
    else:
        bot.send_message(message.from_user.id, answer)
    finally:
        frontier_handler(message)


@bot.message_handler(commands=['moon'])
def moon_handler(message):
    try:
        calls[message.from_user.id]['moon'] += 1
    except KeyError:
        print('User identification error in moon')

    url_moon = 'http://wttr.in/moon'
    bot.send_message(message.from_user.id,
                     requests.get(url_moon, params={'QFT': '', 'lang': 'ru'}).text)
    frontier_handler(message)


@bot.message_handler(commands=['ПРОГНОЗ'])
def weather_tomorrow(message):
    report_buf = []
    print(CURRENT_CITY)
    if report := info_weather.get_weather_list(CURRENT_CITY):
        for count, weather in enumerate(report):
            if count % 6 == 0:
                temp = weather.get_temperature(unit='celsius')['temp']
                date_stamp = weather.get_reference_time('iso').split()
                rep1 = date_stamp[0] + ' Температура: ' + str(round(temp)) + degree_sign + 'C'
                report_buf.append(rep1)
        bot.send_message(message.from_user.id, '\n'.join(report_buf))
        reset_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Не полагай тесть только на прогноз! :) ', reply_markup=reset_markup)
    else:
        bot.send_message(message.from_user.id, 'К сожалению для Вашего местоположения прогноз не доступен! ')
    frontier_handler(message)


def weather_handler(message, city, date=None):
    global CURRENT_CITY
    CURRENT_CITY = city
    try:
        calls[message.from_user.id]['weather'] += 1
    except KeyError:
        print('User identification error in weather')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True, row_width=1)
    button1 = types.KeyboardButton('/ПРОГНОЗ')
    markup.add(button1)
    try:
        if date:
            report = info_weather.get_detailed_report(info_weather.get_weather(city, date))
        else:
            report = info_weather.get_detailed_report(info_weather.get_weather(city))
    except Exception:
        bot.send_message(message.from_user.id, 'Запрашиваемый город не найден')
        frontier_handler(message)
    else:
        if not date:
            report = info_weather.get_detailed_report(info_weather.get_weather(city))
            base_text = f'Температура на сегодня в городе {city.capitalize()} {round(report[0])} {degree_sign}C;\n'
            if not report[1]:
                msg_text = base_text + f'Скорость ветра {report[2]} м/с;\n {report[3]}.'
            else:
                msg_text = base_text + f'{report[1]}, {report[2]} м/с;\n {report[3]}.'

            bot.send_message(message.from_user.id, msg_text, reply_markup=markup)

        #   bot.register_next_step_handler(message, frontier_handler)
        else:  # Very same code / needs to be refactored next
            report = info_weather.get_detailed_report(info_weather.get_weather(city, date))
            base_text = f'Температура на {date} в городе {city.capitalize()} {round(report[0])} {degree_sign}C;\n'
            if not report[1]:
                msg_text = base_text + f'Скорость ветра {report[2]} м/с;\n {report[3]}.'
            else:
                msg_text = base_text + f'{report[1]}, {report[2]} м/с;\n {report[3]}.'
            bot.send_message(message.from_user.id, msg_text, reply_markup=markup)
        # bot.register_next_step_handler(message, frontier_handler)


# This feature will change to automatic city recognize
@bot.message_handler(commands=['Moscow'])
def local__weather(message):
    try:
        calls[message.from_user.id]['weather'] += 1
    except KeyError:
        print('User identification  Key error in weather fixed function')

    city = 'Москва'
    report = info_weather.get_detailed_report(info_weather.get_weather(city))
    base_text = f'Температура на сегодня в городе {city.capitalize()} {round(report[0])} {degree_sign}C;\n'
    if not report[1]:
        msg_text = base_text + f'Скорость ветра {report[2]} м/с;\n {report[3]}.'
    else:
        msg_text = base_text + f'{report[1]}, {report[2]} м/с;\n {report[3]}.'

    bot.send_message(message.from_user.id, msg_text)
    frontier_handler(message)


@bot.message_handler(commands=['calls'])
def calls_handle(message):
    if message.from_user.id not in calls:  # Set to 0 User statistics in an emergency need to be REFACTORED!!!!
        calls[message.from_user.id] = {
            'wiki': 0,
            'weather': 0,
            'moon': 0,
        }
    report = (calls.get(message.from_user.id))
    bot.send_message(message.from_user.id, f'{message.from_user.first_name} Погода {report["weather"]} '
                                           f'Wiki {report["wiki"]} Луна {report["moon"]}')
    frontier_handler(message)


@bot.message_handler(content_types=['text'])
def weather_parser(message):
    today = date.today()
    now = datetime.now()

    msg_string = message.text.lower().split()
    if len(msg_string) == 1:
        print('weather requests', msg_string[0])  # Debug information
        weather_handler(message, msg_string[0])
    elif len(msg_string) == 2:
        try:
            day, month = pares_date(msg_string[1])
        except ValueError:
            bot.send_message(message.from_user.id, 'Неправильный формат даты ... ')
        else:
            try:
                if today.month > month:  # In case of 'Next year'
                    req_date = date(today.year + 1, month, day)
                else:
                    req_date = date(today.year, month, day)
            except ValueError:
                bot.send_message(message.from_user.id, 'Неправильный формат даты ... ')
            else:
                dif = req_date - today
                if 3 < dif.days or dif.days < 0:
                    bot.send_message(message.from_user.id, 'Неправильный формат даты ( в пределах 3-х суток )')
                else:
                    current_shown_dates[message.from_user.id] = req_date  # Selected dates
                    print('Weather request ', msg_string[0], req_date)  # Debug information
                    print(type(req_date))
                    weather_handler(message, msg_string[0], datetime(req_date.year, req_date.month, req_date.day,
                                                                     now.hour, now.minute))

    else:
        bot.send_message(message.from_user.id, 'Я тебя не понял !!!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
