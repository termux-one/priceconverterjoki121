import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

bot = telebot.TeleBot('5686176002:AAELjkeYWFCHneePjIHQkezkQ21O7vHAbd0')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rate_button = types.KeyboardButton('Курсы валют')
    price_button = types.KeyboardButton('Стоимость')
    pay_button = types.KeyboardButton('Готовая выплата')

    markup.row(rate_button, price_button, pay_button)
    bot.send_message(message.chat.id, 'Добро пожаловать, boss!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Курсы валют':
        url_try_rub = 'https://www.banki.ru/products/currency/try/'
        url_usd_rub = 'https://www.banki.ru/products/currency/usd/'

        source = requests.get(url_try_rub)
        soup = BeautifulSoup(source.text, 'html.parser')
        try_rub_current_rate = soup.find('div', {'class': 'currency-table__large-text'})

        source = requests.get(url_usd_rub)
        soup = BeautifulSoup(source.text, 'html.parser')
        usd_rub_current_rate = soup.find('div', {'class': 'currency-table__large-text'})

        try_rub_current_rate = round(float(try_rub_current_rate.text.replace(',', '.')) / 10, 2)
        usd_rub_current_rate = round(float(usd_rub_current_rate.text.replace(',', '.')), 2)

        bot.send_message(message.chat.id, 'Курс (TRY): ' + str(try_rub_current_rate) + ' ₽\n' + 'Курс (USD): ' + str(usd_rub_current_rate) + ' ₽')

    elif message.text == 'Стоимость':
        my_percent = 0.25
        pay_percent = 0.1

        url_try_rub = 'https://www.banki.ru/products/currency/try/'

        source = requests.get(url_try_rub)
        soup = BeautifulSoup(source.text, 'html.parser')
        try_rub_current_rate = soup.find('div', {'class': 'currency-table__large-text'})

        try_rub_current_rate = round(float(try_rub_current_rate.text.replace(',', '.')) / 10, 2)

        price = round(try_rub_current_rate * (1 + my_percent + pay_percent), 2)

        bot.send_message(message.chat.id, 'Стоимость: ' + str(price) + ' ₽')

    elif message.text == 'Готовая выплата':
        bot.send_message(message.chat.id, 'Введите количество лир')

    else:
        try:
            int(message.text)

            url_try_rub = 'https://www.banki.ru/products/currency/try/'
            url_usd_rub = 'https://www.banki.ru/products/currency/usd/'

            source = requests.get(url_try_rub)
            soup = BeautifulSoup(source.text, 'html.parser')
            try_rub_current_rate = soup.find('div', {'class': 'currency-table__large-text'})

            source = requests.get(url_usd_rub)
            soup = BeautifulSoup(source.text, 'html.parser')
            usd_rub_current_rate = soup.find('div', {'class': 'currency-table__large-text'})

            pay_percent = 0.1

            try_rub_current_rate = round(float(try_rub_current_rate.text.replace(',', '.')) / 10, 2)
            usd_rub_current_rate = round(float(usd_rub_current_rate.text.replace(',', '.')), 2)

            pay = round(try_rub_current_rate * (1 + pay_percent), 3)
            amount = int(message.text)

            bot.send_message(message.chat.id, 'Перевести ' + str(round(pay * amount / usd_rub_current_rate, 2)) + ' $')
        except ValueError:
            return

bot.polling(none_stop=True)
