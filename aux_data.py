import os

bot_token = os.environ["TELEGRAM_TOKEN"]

weather_token = os.environ["OWM_TOKEN"]

geo_token = os.environ["GEO_TOKEN"]

GREETING_MSG = '''Приветствую тебя новый пользователь погодного ботика!,
                     тебе доступны следующие команды:
                     /start - начало рабоы с ботом
                     /info - Эта памятка
                     /moon - Информация о луне
                     /Moscow - Тукущая погода авто
                     /wiki - Можно спросить Wiki по Русски!
                     '''
