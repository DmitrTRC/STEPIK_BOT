import telebot
import requests
import pywikibot
import random
from pprint import pprint

token = '1035021917:AAF-3Fki6dWOpQyyTqBbxoFQAEAwYz6fTlk'

site = pywikibot.Site('en', 'wikipedia')

bot = telebot.TeleBot(token)


def weather_request(city='None'):
    url = 'http://wttr.in/'

    if city == 'moon':
        url = url + 'moon' + '?QFT&lang=ru'

    elif city:

        url = url + city + '?format=2'
    else:
        url = url + '?format=2'

    ans = requests.get(url)
    return ans.text


def get_wiki(message, site):
    print(f'Message before request wiki: {message=} ')
    wiki_request = 'Wikipedia:' + message.replace('wiki', '')
    print(wiki_request)
    page = pywikibot.Page(site, wiki_request)
    text = page.text
    print(f'Answered {text=}')
    return text


@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Это бот-погода. Поможет узнать погоду в любом городе. Какой город интересует?'
                         )
    elif message.text in ('привет', 'Hi', 'hi', 'Hi!', 'Привет!', 'привет!'):
        bot.reply_to(message, 'Привет, привет ' + message.from_user.first_name)
    elif message.text.lower() in ('погода на сегодня', 'погода', 'какая погода', 'weather',
                                  'what the weather', 'скажи погоду'):
        bot.send_message(message.chat.id, message.from_user.first_name + ' , а погода сейчас : ' + weather_request())
    elif message.text.lower() == 'москва':
        bot.reply_to(message, 'Сейчас отличная погода! ' + weather_request('Москва'))
    elif message.text.lower().find('город') == 0:
        print('City weather detected')
        weather_message = message.text.lower().replace('город', '')
        print(weather_message.strip())
        bot.send_message(message.chat.id,
                         message.from_user.first_name
                         + ' , а погода сейчас в городе {}: '.format(weather_message.title()) + weather_request(
                             weather_message.strip()))

    elif message.text.lower() in ('луна', 'moon', 'покажи луну', 'show moon'):
        bot.reply_to(message, ' Все о луне что я знаю! ' + weather_request('moon'))
    elif message.text.lower() in ('погода завтра', 'погода на завтра', 'weather for tomorrow'):
        bot.reply_to(message, 'Завтра , будет: еще лучше !( Under construction)')
    elif message.text.lower().split()[0] == 'wiki':

        ans = get_wiki(message.text.lower(), site)
        bot.send_message(message.chat.id, ans)


    else:
        bot.send_message(message.chat.id, 'Я тебя не понял')


bot.polling()
