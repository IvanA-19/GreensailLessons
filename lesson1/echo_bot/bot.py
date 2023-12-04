# Подключаем библиотеки
from telebot import TeleBot
from config import api_token


# Создаем бота на основе класса TeleBot
bot = TeleBot(api_token)


"""
Напишем команду /start с приветствием
Функции бота должны находиться под специальными декораторами. 
В случае обработки сообщений используется декоратор message_handler()
При обработке команд - мы передаем в аргументы декоратора параметр commands со значением списка команд, 
на которые реагирует данный обработчик. Под декоратором располагается функция-обработчик
В случае текстового сообщения она принимает обязательный аргумент message. 
Внутри функции-обработчика start мы записываем в переменную user_name данные пользователя, после отправляем сообщение с
приветствием, используя bot.send_message(), которая принимает два обязательных аргумента: chat_id и текст сообщения 
"""


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    if message.from_user.last_name is not None:
        user_name += f" {message.from_user.last_name}"
    bot.send_message(message.chat.id, f"Hello, {user_name}!")


"""
Теперь напишем эхо-функцию.
Ее синтаксис будет похож на синтаксис функции start, однако в декоратор мы должны передать аргумент content_types
со значением ['text']. После мы говорим боту отправить сообщение с тем же текстом, что нам написали.
"""


@bot.message_handler(content_types=['text'])
def get_echo(message):
    bot.send_message(message.chat.id, message.text)



