from binance.enums import *
from binance.exceptions import *
from utils import get_local_timestamp
import logging
from telegram_message_sender import send_new_buy_order_message


def buy(binance_spot_api, symbol, volume):
    logging.info('trying to buy ' + symbol + ' with volume ' + volume)
    buy_price = extract_buy_price(binance_spot_api, symbol)
    logging.info(symbol + ' buy price is ' + buy_price)
    quantity = volume / buy_price
    logging.info(symbol + ' quantity to buy is ' + quantity)
    order_id = 'b' + get_local_timestamp()
    try:
        logging.info('creating buy order with [' +
                     'symbol: ' + symbol + ', ' +
                     'side: ' + str(SIDE_BUY) + ', ' +
                     'timeInForce: ' + str(TIME_IN_FORCE_GTC) + ', ' +
                     'quantity: ' + str(quantity) + ', ' +
                     'price: ' + str(buy_price) + ', ' +
                     'newClientOrderId: ' + order_id + ', ' +
                     ']')
        send_new_buy_order_message(symbol, buy_price, quantity, order_id)
        buy_order_response = binance_spot_api.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=str(buy_price),
            newClientOrderId=order_id)
        logging.info('buy order response is ' + str(buy_order_response))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        logging.info('error on creating new buy order')
        logging.info(ex)


def extract_buy_price(binance_spot_api, symbol):
    logging.info('trying to get ' + symbol + ' ticker')
    symbol_ticker = binance_spot_api.get_symbol_ticker(symbol=symbol + 'USDT')['price']
    logging.info(symbol + ' ticker :' + symbol_ticker)
    return symbol_ticker
