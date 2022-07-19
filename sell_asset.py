import logging

from binance.enums import *
from binance.exceptions import *

from telegram_message_sender import send_new_sell_order_message
from utils import get_local_timestamp


def sell(binance_spot_api, symbol):
    logging.info('trying to sell ' + symbol)
    volume = binance_spot_api.get_asset_balance(symbol)
    logging.info('volume to sell ' + symbol + ' is ' + str(volume))
    sell_price = extract_sell_price(binance_spot_api, symbol)
    logging.info(symbol + ' sell price is ' + sell_price)
    quantity = volume / sell_price
    logging.info(symbol + ' quantity to sell is ' + quantity)
    order_id = 's' + get_local_timestamp()
    send_new_sell_order_message(symbol, sell_price, quantity, order_id)
    try:
        logging.info('creating sell order with [' +
                     'symbol: ' + symbol + ', ' +
                     'side: ' + str(SIDE_SELL) + ', ' +
                     'timeInForce: ' + str(TIME_IN_FORCE_GTC) + ', ' +
                     'quantity: ' + str(quantity) + ', ' +
                     'price: ' + str(sell_price) + ', ' +
                     'newClientOrderId: ' + order_id + ', ' +
                     ']')
        sell_order_response = binance_spot_api.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=str(sell_price),
            newClientOrderId=order_id)
        logging.info('sell order response is ' + str(sell_order_response))
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as ex:
        logging.error('error on creating new sell order')
        logging.exception(ex)


def extract_sell_price(binance_spot_api, symbol):
    logging.info('trying to get ' + symbol + ' ticker')
    symbol_ticker = binance_spot_api.get_symbol_ticker(symbol=symbol + 'USDT')['price']
    logging.info(symbol + ' ticker :' + symbol_ticker)
    return symbol_ticker
