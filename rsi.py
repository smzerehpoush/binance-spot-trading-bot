from binance.enums import *
from binance.client import Client
import pandas as pd


def calculate_rsi(symbol, start, end, period):
    # [0- open time,
    # 1- open,
    # 2- high,
    # 3- low,
    # 4- close,
    # 5- volume,
    # 6- close time,
    # 7- Quote asset volume,
    # 8- Number of trades,
    # 9-Taker buy base asset volume,
    # 10- Taker buy quote asset volume]
    data = Client().get_historical_klines(
        symbol=symbol + 'USDT',
        interval=KLINE_INTERVAL_1DAY,
        start_str=start,
        end_str=end,
        klines_type=HistoricalKlinesType.SPOT
    )
    for item in data:
        item[1] = float(item[1])
        item[2] = float(item[2])
        item[3] = float(item[3])
        item[4] = float(item[4])
        del item[5:]

    dataframe = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])
    dataframe.set_index('date', inplace=True)

    return rsi(dataframe, period).iloc[-1]


def rsi(df, periods=14, ema=True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi_value = ma_up / ma_down
    return 100 - (100 / (1 + rsi_value))
