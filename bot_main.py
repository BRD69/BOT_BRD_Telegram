import os
from datetime import datetime
from dotenv import load_dotenv

import telebot
from telebot import types

import scripts.wiki as wiki
import scripts.holidays as holidays
import scripts.settings as settings

load_dotenv()

TOKEN = os.getenv('TOKEN')
TOKEN_TEST = os.getenv('TOKEN_TEST')

# TOKEN = '7483399504:AAEduiwd0qwuLafa-iyczXaK-AGlg5B0RE8'
# TOKEN_TEST = '7214000002:AAFt1hoM90lzM_CDJxGW_26Q-BGoLTf1uec'

bot = telebot.TeleBot(TOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand('start', 'Старт бота'),
        telebot.types.BotCommand('wiki', 'Случайная статья на Wiki'),
        telebot.types.BotCommand('holiday', 'Праздники сегодня'),
        telebot.types.BotCommand('help', 'Помощь'),
    ]
)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.clear_step_handler(message)
    it_test = ""
    if bot.token == TOKEN_TEST:
        it_test = "TEST"
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id
    text_message = f"Привет, я BRD бот! {it_test}"

    bot.send_message(chat_id, text=text_message, message_thread_id=message_thread_id, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id
    text_message = (f"*Примеры команд*\n\n"
                    f"time 09:00 - уставка времени получения сообщения")
    bot.send_message(chat_id, text=text_message, message_thread_id=message_thread_id, parse_mode='Markdown')


@bot.message_handler(commands=['wiki'])
def handle_wiki(message):
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id

    title, url, img_link, summary = wiki.get_wiki_data()

    keyboard = types.InlineKeyboardMarkup()
    key_add_to_group = types.InlineKeyboardButton(text='Wiki', url=url)
    keyboard.add(key_add_to_group)

    text_message = (f"*{title}*\n\n"
                    f"{summary}")

    # bot.delete_message(message.chat.id, message.message_id - 1)

    if img_link:
        bot.send_photo(chat_id=chat_id, photo=img_link, caption=text_message, message_thread_id=message_thread_id,
                       reply_markup=keyboard, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text=text_message, message_thread_id=message_thread_id, reply_markup=keyboard,
                         parse_mode='Markdown')


@bot.message_handler(commands=['holiday'])
def handle_holiday(message):
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id
    list_holidays = holidays.get_holidays()

    text_message = '\n'.join(list_holidays)
    text_message += f'\n\n{datetime.now().strftime("%d.%m")}'

    bot.send_message(chat_id, text=text_message, message_thread_id=message_thread_id, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def send_message(message):
    if 'time' in message.text:
        result = settings.set_time_send_message(message.text)
        if result['status'] == 'ok':
            text_message = f"Время отправки поста Wiki установлено на *{result['text']}*"
        else:
            text_message = f'{result["text"]}'
        bot.reply_to(message, text_message, parse_mode='Markdown')
    else:
        bot.reply_to(message, 'Введите корректный текст команду')


if __name__ == '__main__':
    bot.polling(none_stop=True)
