from binance.enums import *
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def calculate_rsi(symbol, start_date, end_date, period):
    data = Client().get_historical_klines(
        symbol=symbol + 'USDT',
        interval=KLINE_INTERVAL_1DAY,
        start_str=start_date,
        end_str=end_date,
        klines_type=HistoricalKlinesType.SPOT
    )
    data_frame = pd.DataFrame(data)
    data_frame = data_frame.iloc[:, 1:6]
    data_frame.columns = ['open', 'high', 'low', 'close', 'volume']
    data_frame = data_frame.astype(float)
    print(rsi_tradingview(data_frame, period))


def rsi_tradingview(ohlc: pd.DataFrame, period: int = 14, round_rsi: bool = True):
    delta = ohlc["close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm(up, alpha=1 / period).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha=1 / period).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    return np.round(rsi, 2)[-1] if round_rsi else rsi[-1]
