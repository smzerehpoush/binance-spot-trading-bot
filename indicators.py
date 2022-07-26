from datetime import datetime, timedelta

from heikin_ashi import calculate_heikin_ashi
from rsi import calculate_rsi


def rsi_fourteen_days_close(symbol):
    start = (datetime.utcnow() - timedelta(days=1000)).strftime('%d %b %Y')
    end = (datetime.utcnow() - timedelta(days=1)).strftime('%d %b %Y')
    return calculate_rsi(symbol, start, end, 14)


def rsi_fifteen_days_close(symbol):
    start = (datetime.utcnow() - timedelta(days=1000)).strftime('%d %b %Y')
    end = (datetime.utcnow() - timedelta(days=2)).strftime('%d %b %Y')
    return calculate_rsi(symbol, start, end, 14)


def heikin_today(symbol):
    start = (datetime.utcnow() - timedelta(days=1000)).strftime('%d %b %Y')
    end = datetime.utcnow().strftime('%d %b %Y')
    candle = calculate_heikin_ashi(symbol, start, end)
    return candle.close - candle.open


def heikin_yesterday(symbol):
    start = (datetime.utcnow() - timedelta(days=1000)).strftime('%d %b %Y')
    end = (datetime.utcnow() - timedelta(days=1)).strftime('%d %b %Y')
    candle = calculate_heikin_ashi(symbol, start, end)
    return candle.close - candle.open


def heikin_day_before_yesterday(symbol):
    start = (datetime.utcnow() - timedelta(days=1000)).strftime('%d %b %Y')
    end = (datetime.utcnow() - timedelta(days=2)).strftime('%d %b %Y')
    candle = calculate_heikin_ashi(symbol, start, end)
    return candle.close - candle.open
