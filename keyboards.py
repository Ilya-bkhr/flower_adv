from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

def no_keyboard():
      keyboard =  ReplyKeyboardRemove()
      return keyboard

def first_keyboard():
        keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("Предоставить номер телефона", request_contact= True)],
        [KeyboardButton("Отправить номер текстом")]
        ], resize_keyboard=True)
        return keyboard


def second_keyboard():
        keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("Выбрать рекламодателя")],
        [KeyboardButton('Профиль')], [KeyboardButton('Вывод средств')]
        ], resize_keyboard=True)
        return keyboard


def choose_website():
        keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('все-тюльпаны.рф', callback_data='xn----8sbem5anmml8ghw.xn--p1ai')]
        ])
        return keyboard


# keyboard = InlineKeyboardMarkup([
#         [InlineKeyboardButton('все-тюльпаны.рф', callback_data='xn----8sbem5anmml8ghw.xn--p1ai')],
#         [InlineKeyboardButton('тюльпаны-москва.рф', callback_data='xn----7sbbh3bdjglf1ae5jk2a.xn--p1ai')],
#         [InlineKeyboardButton('tylpanov77.ru', callback_data='tylpanov77.ru')],
#         [InlineKeyboardButton('tylpanov.ru', callback_data='tylpanov.ru')]
#         ])
