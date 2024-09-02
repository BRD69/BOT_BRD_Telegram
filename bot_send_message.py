"""
Отправка по расписанию
"""

import schedule
import time
import telebot

import scripts.settings as settings_bot


TOKEN = '7483399504:AAEduiwd0qwuLafa-iyczXaK-AGlg5B0RE8'
TOKEN_TEST = '7214000002:AAFt1hoM90lzM_CDJxGW_26Q-BGoLTf1uec'

bot = telebot.TeleBot(TOKEN)


def get_time():
    settings = settings_bot.Settings()
    settings.load()
    return settings.time


def correct_time():
    settings = settings_bot.Settings()
    settings.load()
    return settings.correct_time()


def send_message():
    chat_id = -1002213295028
    message_thread_id = 55
    text_message = ("*Отправка тест сообщения*\n\n"
                    "Вот само сообщение")

    bot.send_message(chat_id, text=text_message, message_thread_id=message_thread_id, parse_mode='Markdown')


schedule.every().day.at(get_time()).do(send_message)

while True:
    if correct_time():
        schedule.run_pending()
    time.sleep(1)
