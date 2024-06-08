from telebot import types
from language.keyboard_lang import *
def generate_language():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_eng = types.KeyboardButton(text="🇺🇸EN")
    btn_rus = types.KeyboardButton(text="🇷🇺RU")
    keyboard.row(btn_eng, btn_rus)
    return keyboard
def generate_main_menu(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_laptop = types.KeyboardButton(text=menu_laptop[lang])
    btn_monitor = types.KeyboardButton(text=menu_monitor[lang])
    btn_mono = types.KeyboardButton(text=menu_monoblok[lang])
    keyboard.row(btn_laptop, btn_monitor, btn_mono)
    return keyboard


def generate_inline_url(lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_more_bay = types.InlineKeyboardButton(text=buy[lang], callback_data="buy")
    keyboard.row(btn_more_bay)
    return keyboard


def generate_pagination(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_next = types.KeyboardButton(text=pagination_forward[lang])
    btn_prev = types.KeyboardButton(text=pagination_back[lang])
    btn_menu = types.KeyboardButton(text=pagination_menu[lang])
    keyboard.row(btn_prev, btn_next)
    keyboard.row(btn_menu)
    return keyboard