from binance.enums import *
from binance.client import Client


def calculate_heikin_ashi(symbol, start, end):
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

    def ha_low(row):
        return min(float(data[row][3]), float(data[row][1]), float(data[row][4]))

    def ha_high(row):
        return max(float(data[row][2]), float(data[row][1]), float(data[row][4]))

    def ha_op(row):
        return (float(data[row - 1][1]) + float(data[row - 1][4])) / 2

    def ha_close(row):
        return (float(data[row][1]) + float(data[row][2]) + float(data[row][3]) + float(data[row][4])) / 4

    ha_candle = []
    for x in range(len(data) - 1):
        x += 1
        ha_candle.append({
            'low': ha_low(x),
            'high': ha_high(x),
            'open': ha_op(x),
            'close': ha_close(x)
        })

    return ha_candle
