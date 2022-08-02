from binance.enums import *
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def calculate_heikin_ashi(symbol, start_date, end_date):
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
    print(heikin_ashi_tradingview(data_frame))


def heikin_ashi_tradingview(df: pd.DataFrame):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])

    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)

    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)

    return heikin_ashi_df.iloc[-1]
