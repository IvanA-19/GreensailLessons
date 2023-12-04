# Подключаем библиотеки.
# Для клавиатур нам понадобится подключить еще несколько классов
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from config import api_token, help_list


# Создаем бота на основе класса TeleBot
bot = TeleBot(api_token)


"""
Напишем функцию для получения reply_клавиатуры. 
Reply клавиатура - клавиатура, которая подразумевает ответ бота на сообщение, присланное при нажатии на кнопку.
Для того, чтобы клавиатуры имела нормальный вид - ставим аргумент resize_keyboard в значение True.
Если мы хотим расположить несколько кнопок в одном ряду - то их необходимо добавить одновременно с помощью add()
Также наша функция будет принимать список с именами кнопок и параметр one_time, отвечающий за исчезновение клавиатуры 
при нажатии на кнопку
"""


def get_reply_keyboard(buttons: list = None, one_time: bool = True, menu: bool = False) -> ReplyKeyboardMarkup | None:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    if menu:
        keyboard.add(KeyboardButton("Какая-то кнопка"))
        keyboard.add(KeyboardButton("Команды"), KeyboardButton("Выход"))
        return keyboard
    elif buttons:
        for button in buttons:
            keyboard.add(KeyboardButton(button))
        return keyboard
    return


"""
Теперь напишем функцию для получения inline клавиатуры
Inline клавиатура - клавиатура, которая подразумевает выполнение действий в случае успешной обработки callback_data, 
уникальной для каждой кнопки. В данном случае при нажатии на кнопку - в программу возвращается так-называемый коллбэк,
который мы перехватываем и обрабатываем. Данная клавиатура не подразумевает аргументов one_time_keyboard 
и resize_keyboard. Наша функция будет принимать два аргумента: список названий кнопок и список callback
"""


def get_inline_keyboard(buttons: list = None, callbacks: list = None) -> InlineKeyboardMarkup | None:
    keyboard = InlineKeyboardMarkup()
    if buttons and callbacks and len(buttons) == len(callbacks):
        for button, callback in zip(buttons, callbacks):
            keyboard.add(InlineKeyboardButton(button, callback_data=callback))
        return keyboard
    return


"""
Напишем команду /start с приветствием
Функции бота должны находиться под специальными декораторами. 
В случае обработки сообщений используется декоратор message_handler()
При обработке команд - мы передаем в аргументы декоратора параметр commands со значением списка команд, 
на которые реагирует данный обработчик. Под декоратором располагается функция-обработчик
В случае текстового сообщения она принимает обязательный аргумент message. 
Внутри функции-обработчика start мы записываем в переменную user_name данные пользователя, после отправляем сообщение с
приветствием, используя bot.send_message(), которая принимает два обязательных аргумента: chat_id и текст сообщения
Так же передадим аргумент reply_markup, который прикрепит к сообщению нашу клавиатуру
"""


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    if message.from_user.last_name is not None:
        user_name += f" {message.from_user.last_name}"
    keyboard = get_reply_keyboard(['Меню'])
    bot.send_message(message.chat.id, f"Hello, {user_name}!", reply_markup=keyboard)


# По такому же принципу напишем остальные команды
@bot.message_handler(commands=['help'])
def get_command_list(message):
    keyboard = get_reply_keyboard(['СТАРТ'])
    bot.send_message(message.chat.id, "До свидания!", reply_markup=keyboard)


@bot.message_handler(commands=['some_button'])
def process_some_button(message):
    keyboard = get_reply_keyboard(['Меню'])
    bot.send_message(message.chat.id, "Обработка какой-то кнопки", reply_markup=keyboard)


@bot.message_handler(commands=['exit'])
def finish_work(message):
    keyboard = get_reply_keyboard(['СТАРТ'])
    bot.send_message(message.chat.id, "До свидания!", reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def open_menu(message):
    keyboard = get_reply_keyboard(menu=True)
    bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboard)


"""
Теперь напишем эхо-функцию.
Ее синтаксис будет похож на синтаксис функции start, однако в декоратор мы должны передать аргумент content_types
со значением ['text']. 
Далее обработаем значение текста, присвоенное кнопкам нашей клавиатуры, а также сделаем проверку на неизвестный боту 
текст
"""


@bot.message_handler(content_types=['text'])
def get_echo(message):
    if message.text.lower() == "меню":
        keyboard = get_reply_keyboard(menu=True)
        bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboard)
    elif message.text.lower() == "какая-то кнопка":
        keyboard = get_inline_keyboard(['Редактировать', 'Удалить'], ['edit', 'delete'])
        bot.send_message(message.chat.id, "Обработка какой-то кнопки", reply_markup=keyboard)
    elif message.text.lower() == "команды":
        keyboard = get_reply_keyboard(['Меню'])
        bot.send_message(message.chat.id, f"Доступные команды: {help_list}", reply_markup=keyboard)
    elif message.text.lower() == "выход":
        keyboard = get_reply_keyboard(['СТАРТ'])
        bot.send_message(message.chat.id, "До свидания!", reply_markup=keyboard)
    elif message.text.lower() == "старт":
        user_name = message.from_user.first_name
        if message.from_user.last_name is not None:
            user_name += f" {message.from_user.last_name}"
        keyboard = get_reply_keyboard(['Меню'])
        bot.send_message(message.chat.id, f"Hello, {user_name}!", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Прости, я не понимаю!\nЧтобы открыть меню - нажми кнопку\n"
                                          "Чтобы открыть список команд - используй /help")


"""
Напишем обработчик коллбэков. Он похож на обработчик сообщений, однако теперь будет использоваться декоратор 
callback_query_handler() с аргументом func=lambda call: True
Вместо сообщения функция в нем принимает аргумент call, который в свою очередь содержит в себе message
"""


@bot.callback_query_handler(func=lambda call: True)
def check_callback(call):
    # Отредактируем текст сообщения
    if call.data == 'edit':
        """
        Функция редактирования сообщения принимает три обязательных аргумента:
        text, chat_id, message_id
        также можно добавить аргумент reply_markup
        """
        keyboard = get_inline_keyboard(['Удалить'], ['delete'])
        bot.edit_message_text("`Косая кавычка`", call.message.chat.id, call.message.id, reply_markup=keyboard)
    # Удалим текущее сообщение и отправим вместо него новое
    elif call.data == 'delete':
        # Функция удаления сообщения принимает два обязательных аргумента: chat_id, message_id
        bot.delete_message(call.message.chat.id, call.message.id)
        keyboard = get_reply_keyboard(['Меню'])
        bot.send_message(call.message.chat.id, "Клавиатуры это просто!", reply_markup=keyboard)
