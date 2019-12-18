import telebot
from Dispatcher import *
from aux_data import bot_token  # Telegram API KEY, GEO API, , Weather API , extra data

bot = telebot.TeleBot(bot_token)
calls = {}  # User statistics


def do_start(message):
    print('Start function')


def do_info():
    pass


def do_calls():
    pass


def do_greeting():
    pass


def do_moon():
    pass


def do_wiki():
    pass


task = CDispatcher({
    '/start': do_start,
    '/info': do_info,
    '/calls': do_calls,
    'привет': do_greeting,
    'луна': do_moon,
    'wiki': do_wiki,
})  # Menu task handler@bot.message_handler(func=lambda message: True)


@bot.message_handler(func=lambda message: True, commands=['help'])
def frontier_handler(message):
    if (user_id := message.from_user.id) not in calls:  # Set to 0 User statistics if not found in calls
        calls[user_id] = 0
        bot.send_message(message.chat.id, 'Это бот-погода. Поможет узнать погоду в любом городе. /help - помощь ')
        if task.is_command(message.text.lower()):
            task.run(message.text.lower(), message)


def info_handler(message)


    @bot.message_handler(commands=['start'])
    def main_handler(message):
        bot.send_message(message.chat.id, 'Введите город и дату в предела 3 суток.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
