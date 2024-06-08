

from telebot import TeleBot
from telebot.types import LabeledPrice
from language.bot_lang import *
from keyboards import *
from repository.db_laptop import Postgres
from repository.db_monitor import Postgres_monitor
from repository.db_monoblok import Postgres_monoblok
token = "7280023472:AAEZyEluhQ1x9-sF3fDfC4jxfmsGIux94O4"
click_token = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"
bot = TeleBot(token)
user_lang = {}
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    lang = bot.send_message(chat_id, "Choose language", reply_markup=generate_language())
    bot.register_next_step_handler(lang, menu)
def menu(message):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id)
    photo = open('local_media/img_1.png', 'rb')
    if message.text == "🇺🇸EN":
        lang = 'en'
        bot.send_photo(chat_id, photo, caption=caption[lang])
    if message.text == "🇷🇺RU":
        lang = 'ru'
        bot.send_photo(chat_id, photo, caption=caption[lang])
    bot.register_next_step_handler(message, choose_catalog)
    user_lang[chat_id] = lang
def choose_catalog(message):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id)
    catalog = bot.send_message(chat_id, sel_catalogs[lang], reply_markup=generate_main_menu(lang))
    bot.register_next_step_handler(catalog, main_catalogs)

def main_catalogs(message,product_id = 0,products = None ):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id)
    if message.text == pagination_menu[lang]:
        return choose_catalog(message)

    if message.text == menu_laptop[lang]:
        products = Postgres().select_data()

    if message.text == menu_monitor[lang]:
        products = Postgres_monitor().select_data()

    if message.text == menu_monoblok[lang]:
        products = Postgres_monoblok().select_data()

    if message.text == pagination_forward[lang] and product_id < len(products):
        product_id += 1

    elif message.text == pagination_back[lang] and product_id > 0:
        product_id -= 1


    product = products[product_id]
    product_title = product[0]
    photo = product[1]
    product_description = product[2]
    product_price = product[3]
    bot.send_photo(chat_id, photo, caption=f'{name[lang]}: {product_title}\n\n'
                                               f'{character[lang]}: {product_description}'
                                               f'\n\n{price[lang]}: {product_price}',
                                    reply_markup=generate_inline_url(lang))


    user_message = bot.send_message(chat_id, f"{reserve[lang]} : {len(products) - (product_id + 1)}", reply_markup=generate_pagination(lang))

    if message.text == pagination_forward[lang] and len(products) - (product_id + 1) == 0:
        bot.send_message(chat_id, "No products!")
        product_id = product_id - len(products)  # -1
    bot.register_next_step_handler(user_message, main_catalogs, product_id, products)


@bot.callback_query_handler(func=lambda call: True)
def payments(call):
    chat_id = call.message.chat.id
    product_price_data = ''
    if call.data == "buy":
        product_info = call.message.caption
        product = product_info.split(':')
        product_name = product[1].replace("Characteristics", "")
        description = product[3].replace("Price", "")
        product_price = product[-1].replace('сум', "")  # " 2 700 00" -> "270000"
        for x in product_price:
            if x.isdigit():
                product_price_data += x
        INVOICE = {
            "title": product_name,
            "description": description,
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": click_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_name, amount=int(product_price_data + '00'))]
        }

        bot.send_invoice(chat_id, **INVOICE)
        bot.register_next_step_handler(call.message, successful_payment)

@bot.pre_checkout_query_handler(func=lambda query: True)
def invoice_checkout(query):
    """ Проверка чека """
    bot.answer_pre_checkout_query(query.id, ok=True, error_message="Error !")


def successful_payment(message):
    """ Отправить сообщение о успешной оплате """
    bot.send_message(message.chat.id, "Payment was successfully performed!")
    return choose_catalog(message)


bot.polling(none_stop=True)