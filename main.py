from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from buy_asset import buy
from config import BINANCE_API_TIMEOUT, MAXIMUM_NUMBER_OF_API_CALL_TRIES, ACTIVE_TRADING_SYMBOLS, \
    WALLET_USAGE_PERCENT
from credentials import BINANCE_API_KEY, BINANCE_SECRET_KEY
from indicators import rsi_fourteen_days_close, rsi_fifteen_days_close, heikin_today, heikin_yesterday, \
    heikin_day_before_yesterday
from return_codes import *
from sell_asset import sell
from telegram_message_sender import send_message
import logging
import sys

global executing_times_file
global binance_spot_api
global account_free_usdt_balance
global last_account_free_usdt_balances_list
global account_locked_usdt_balance
global last_account_locked_usdt_balances_list
global heikin_ashi_candles


def is_it_time_to_sell(symbol: str):
    logging.info('checking to is it time to sell symbol ' + symbol)
    suitable: False  # You should define your sell strategy here
    if suitable:
        logging.info('it is time to sell symbol ' + symbol)
    else:
        logging.info('it is not time to sell symbol ' + symbol)
    return suitable


def is_it_time_to_to_buy(symbol: str):
    logging.info('checking to is it time to buy symbol ' + symbol)
    suitable: False  # You should define your BUY strategy here
    if suitable:
        logging.info('it is time to buy symbol ' + symbol)
    else:
        logging.info('it is not time to buy symbol ' + symbol)
    return suitable


def is_binance_status_ok():
    logging.info('checking binance status')
    status: bool = binance_spot_api.get_system_status()['status'] == 0
    logging.info('binance status is ' + str(status))
    return status


def update_account_usdt_balance():
    logging.info('trying to update account USDT balance')
    global account_free_usdt_balance
    global last_account_free_usdt_balances_list
    last_account_free_usdt_balances_list = []
    global account_locked_usdt_balance
    global last_account_locked_usdt_balances_list
    last_account_locked_usdt_balances_list = []
    for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
        try:
            logging.info('trying to get USDT balance')
            asset_balance_response = binance_spot_api.get_asset_balance('USDT')
            logging.info('USDT balance is' + str(asset_balance_response))
            if asset_balance_response is None:
                return ASSET_BALANCE_NOT_FOUND
            account_free_usdt_balance = float(asset_balance_response['free'])
            logging.info('account free usdt balance is ' + str(account_free_usdt_balance))
            last_account_free_usdt_balances_list.append(account_free_usdt_balance)

            account_locked_usdt_balance = float(asset_balance_response['locked'])
            logging.info('account locked usdt balance is ' + str(account_locked_usdt_balance))
            last_account_locked_usdt_balances_list.append(account_locked_usdt_balance)
            return SUCCESSFUL
        except (BinanceRequestException, BinanceAPIException) as ex:
            logging.error('ERROR in update_account_usdt_balance')
            logging.exception(ex)
            return ERROR


def init_bot():
    global binance_spot_api
    global executing_times_file
    binance_spot_api = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY,
                              requests_params={'timeout': BINANCE_API_TIMEOUT})
    logging.info('initiating bot...')
    executing_times_file = open('execute-times.tmp', 'a+')


def sell_symbols(to_sell_symbols):
    for symbol in to_sell_symbols:
        sell(binance_spot_api, symbol)


def buy_symbols(to_buy_symbols_with_weights):
    global account_free_usdt_balance
    total_weight = 0
    for item in to_buy_symbols_with_weights:
        total_weight += item['weight']

    total_buy_volume = WALLET_USAGE_PERCENT / 100 * account_free_usdt_balance
    for item in to_buy_symbols_with_weights:
        volume = item['weight'] / total_weight * total_buy_volume
        buy(binance_spot_api, item['symbol'], volume)


def check_for_buy_and_sell_symbols(to_buy_symbols, to_sell_symbols):
    logging.info('checking for buy and sell symbols...')
    for item in ACTIVE_TRADING_SYMBOLS:
        symbol = item['symbol']
        if is_it_time_to_sell(symbol):
            to_sell_symbols.append(symbol)
        if is_it_time_to_to_buy(symbol):
            to_buy_symbols.append({'symbol': symbol, 'weight': item['weight']})


def does_run_this_day():
    global executing_times_file
    content = executing_times_file.read()
    return content.__contains__(datetime.now().strftime('%Y-%m-%d'))


def update_executing_times_file():
    global executing_times_file
    executing_times_file.write(datetime.now().strftime('%Y-%m-%d'))


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p',
                        handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
    init_bot()

    while True:
        if not is_binance_status_ok():
            continue
        send_message('bot started')
        if does_run_this_day():
            logging.info('bot already was ran at this day')
            return
        update_account_usdt_balance()
        to_sell_symbols = []
        to_buy_symbols_with_weights = []
        check_for_buy_and_sell_symbols(to_buy_symbols_with_weights, to_sell_symbols)
        sell_symbols(to_sell_symbols)
        buy_symbols(to_buy_symbols_with_weights)
        update_executing_times_file()
        return


if __name__ == '__main__':
    main()
