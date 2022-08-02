import logging

import telegram

from config import SEND_TELEGRAM_MESSAGE, TELEGRAM_USER_ID_LIST
from credentials import TELEGRAM_API_KEY

telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)


def send_new_buy_order_message(symbol, buy_price, quantity, order_id):
    send_message(
        'creating buy order with [\n' +
        'symbol: ' + symbol + ', \n' +
        'timeInForce: ' + 'TIME_IN_FORCE_GTC' + ', \n' +
        'quantity: ' + str(quantity) + ', \n' +
        'price: ' + str(buy_price) + ', \n' +
        'newClientOrderId: ' + order_id + '\n' +
        ']'
    )


def send_new_sell_order_message(symbol, sell_price, quantity, order_id):
    send_message(
        'creating sell order with [\n' +
        'symbol: ' + symbol + ', \n' +
        'timeInForce: ' + 'TIME_IN_FORCE_GTC' + ', \n' +
        'quantity: ' + str(quantity) + ', \n' +
        'price: ' + str(sell_price) + ', \n' +
        'newClientOrderId: ' + order_id + '\n' +
        ']'
    )


def send_message(message):
    if not SEND_TELEGRAM_MESSAGE:
        logging.info('sending telegram messages is disabled')
        return
    for TELEGRAM_USER_ID in TELEGRAM_USER_ID_LIST:
        try:
            telegram_bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
        except telegram.error.TelegramError as ex:
            logging.error("error in sending message to telegram")
            logging.exception(ex)


if __name__ == '__main__':
    send_new_buy_order_message('BTCUSDT', '10000', 1, 'b347239423984729')
