import telebot
import t_token  # Telegram API KEY


class MyBot:
    def __init__(self):
        self.bot = telebot.TeleBot(t_token.bot_token)
        self.calls = {}  # User statistics
        self.GREETING_MSG = '''Приветствую тебя новый пользователь погодного ботика!,
                     тебе доступны следующие команды:
                     /start - начало рабоы с ботом
                     /info - Эта памятка
                     город,
                     город дата ( день.месяц ) не дальше 3-х дней,
                     луна ( moon ),
                     wiki ( вики ) запрос'''

    @bot.message_handler(func=lambda message: True)
    def frontier_handler(message):
        user_id = message.from_user.id
        if user_id not in calls:
            calls[user_id] = 0
