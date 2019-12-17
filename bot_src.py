import telebot
import aux_data  # Telegram API KEY


class CDispatcher:
    def __init__(self, table=None):
        if not table:
            self.task_manager = {}
        else:
            self.task_manager = table

    def is_command(self, command):
        pass


class CWeatherBot:
    bot = telebot.TeleBot(aux_data.bot_token)

    def __init__(self):
        self.calls = {}  # User statistics
        self.task = CDispatcher()  # Menu task handler


    @bot.message_handler(func=lambda message: True)
    def frontier_handler(self, message):
        if (user_id := message.from_user.id) not in self.calls:  # Set to 0 User statistics if not found in calls
            self.calls[user_id] = 0
            self.bot.send_message(message.chat.id, 'Это бот-погода. Поможет узнать погоду в любом городе. ')
