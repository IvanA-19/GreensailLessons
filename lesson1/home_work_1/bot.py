from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from config import *
from time import sleep
from random import randint


bot = TeleBot(api_token)


def get_reply_keyboard(buttons: list[str | int] = None, one_time: bool = True, menu: bool = False) -> ReplyKeyboardMarkup | None:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    if menu:
        keyboard.add(KeyboardButton('Играть'))
        keyboard.add(KeyboardButton('Помощь'), KeyboardButton('Выход'))
        return keyboard
    elif buttons:
        for button in buttons:
            keyboard.add(button)
        return keyboard
    return


def get_inline_keyboard(buttons: list[str | int] = None, callbacks: list[int | str] = None) -> InlineKeyboardMarkup | None:
    keyboard = InlineKeyboardMarkup()
    if buttons and callbacks and len(buttons) == len(callbacks):
        for button, callback in zip(callbacks, buttons):
            keyboard.add(InlineKeyboardButton(button, callback))
        return keyboard
    return


def send_action(chat_id: int | str, action: str, time: int = 2) -> None:
    sleep(time)
    bot.send_chat_action(chat_id, action)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = get_reply_keyboard(['Меню'], one_time=False)
    user_name = message.from_user.first_name
    if message.from_userlast_name is not None:
        user_name += f" {message.from_user.last_name}"
    send_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, f"Hello, {user_name}", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def get_help_list(message):
    keyboard = get_reply_keyboard(['Меню'], one_time=False)
    send_action(message.chat.id, "typing", time=3)
    bot.send_message(message.chat.id, f"Список доступных команд: {help_list}", reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def open_menu(message):
    keyboard = get_reply_keyboard(menu=True)
    send_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Выберите, что вы хотите сделать", reply_markup=keyboard)


@bot.message_handler(commands=['play'])
def play_game(message):
    num = randint(0, 10)
    num_vars = [i + num for i in range(-2, 3)]
    num_callbacks = [i for i in range(6)]
    keyboard = get_inline_keyboard(num_vars, num_callbacks)
    send_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Я загадал число в промежутке от 0 до 10. Попробуй угадать, какое число"
                                      " я загадал", reply_markup=keyboard)


@bot.message_handler(commands=['exit'])
def finish_work(message):
    keyboard = get_reply_keyboard(['СТАРТ'])
    send_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "До свидания!", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text.lower() == 'старт':
        keyboard = get_reply_keyboard(['Меню'], one_time=False)
        user_name = message.from_user.first_name
        if message.from_userlast_name is not None:
            user_name += f" {message.from_user.last_name}"
        send_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, f"Hello, {user_name}", reply_markup=keyboard)

    elif message.text.lower() == "меню":
        keyboard = get_reply_keyboard(menu=True)
        send_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Выберите, что вы хотите сделать", reply_markup=keyboard)

    elif message.text.lower() == "помощь":
        keyboard = get_reply_keyboard(['Меню'], one_time=False)
        send_action(message.chat.id, "typing", time=3)
        bot.send_message(message.chat.id, f"Список доступных команд: {help_list}", reply_markup=keyboard)

    elif message.text.lower() == "играть:"
        num = randint(0, 10)
        num_vars = [i + num for i in range(-2, 3)]
        num_callbacks = [i for i in range(6)]
        keyboard = get_inline_keyboard(num_vars, num_callbacks)
        send_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Я загадал число в промежутке от 0 до 10. Попробуй угадать, какое число"
                                          " я загадал", reply_markup=keyboard)

    elif message.text.lower() == "выход":
        keyboard = get_reply_keyboard(['СТАРТ'])
        send_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "До свидания!", reply_markup=keyboard)

    else:
        send_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "Прости, но я не понимаю. Используй /help для просмотра списка команд")


@bot.callback_query_handler(func=lambda call: True)
def check_callback(call):
    if call.data == 2:
        keyboard = get_reply_keyboard(['Меню'])
        bot.edit_message_text("Поздравляю, ты угадал!", call.message.chat.id, call.mesage.id,
                              reply_markup=keyboard)

    elif call.data == "try_again":
        num = randint(0, 10)
        num_vars = [i + num for i in range(-2, 3)]
        num_callbacks = [i for i in range(6)]
        bot.delete_message(call.message.chat.id, call.message.id)
        keyboard = get_inline_keyboard(num_vars, num_callbacks)
        send_action(call.message.chat.id, "typing")
        bot.send_message(call.message.chat.id, "Я загадал число в промежутке от 0 до 10. Попробуй угадать, какое число"
                                          " я загадал", reply_markup=keyboard)
    else:
        keyboard = get_inline_keyboard(['Попробовать еще раз'], ['try_again'])
        bot.edit_message_text("К сожалению, ты не угадал. Попробуй еще раз!", call.message.chat.id,
                              call.message.id,reply_markup=keyboard)
