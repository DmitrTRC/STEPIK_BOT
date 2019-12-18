import telebot
from Dispatcher import *
from aux_data import *  # Telegram API KEY, GEO API, , Weather API , extra data

bot = telebot.TeleBot(bot_token)
calls = {}  # User statistics

task = CDispatcher({

})  # Menu task handler@bot.message_handler(func=lambda message: True)


@bot.message_handler(func=lambda message: True, commands='start')
def frontier_handler(message):
    print(f'Write frontier handling starting... {message.from_user.id=}')
    if message.from_user.id not in calls:  # Set to 0 User statistics if not found in calls
        calls[message.from_user.id] = 0
        bot.send_message(message.chat.id, 'Это бот-погода. Поможет узнать погоду в любом городе. /info - помощь ')
    else:
        calls[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Введите город и дату в предела 3 суток.')


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_message(message.from_user.id, GREETING_MSG)


@bot.message_handler(commands=['calls'])
def calls_handle(message):
    bot.send_message(message.from_user.id, message.from_user.first_name + ' ' + str(calls.get(message.from_user.id)))


if __name__ == '__main__':
    bot.polling(none_stop=True)
