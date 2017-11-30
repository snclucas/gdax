import os

import pandas as pd

from data import gdax_data
from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def get_data(granularity=3600, max_=200):
    eth_data = gdax_data.get_data("ETH-USD", granularity, max_)
    btc_data = gdax_data.get_data("BTC-USD", granularity, max_)
    ltc_data = gdax_data.get_data("LTC-USD", granularity, max_)

    eth_df = pd.DataFrame(list(reversed(eth_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    btc_df = pd.DataFrame(list(reversed(btc_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    ltc_df = pd.DataFrame(list(reversed(ltc_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    return {"eth": eth_df, "btc": btc_df, "ltc": ltc_df}


def check_engulfing(df):
    df['engulfing'] = df.apply(lambda x:
                               check_engulfing_func(x['low'], x['high'], x['open'], x['close'],
                                                    x.shift(1)['low'], x.shift(1)['high'], x.shift(1)['open'],
                                                    x.shift(1)['close']), axis=1)


def check_hammer(df):
    df['hammer'] = df.apply(lambda x:
                            check_hammer_func(x['low'], x['high'], x['open'], x['close']), axis=1)


def check_doji(df):
    df['doji'] = df.apply(lambda x:
                          check_doji_func(x['low'], x['high'], x['open'], x['close']), axis=1)


def check_engulfing_func(cur_low, cur_high, cur_open, cur_close, prev_low, prev_high, prev_open, prev_close):
    if cur_close >= cur_open and prev_close < prev_open:
        if cur_open > prev_open and cur_close < prev_close:
            if cur_high > prev_high and cur_low < prev_low:
                return True
    return False


def check_hammer_func(cur_low, cur_high, cur_open, cur_close):
    if cur_close >= cur_open:
        if cur_close >= cur_high:
            if (cur_open - cur_low) > 2 * (cur_close - cur_open):
                return True
    return False


def check_doji_func(cur_low, cur_high, cur_open, cur_close):
    if cur_high > cur_close:
        if cur_low < cur_open:
            if cur_close / cur_open < 1.0001:
                return True
    return False


def correlation(crypto_data, lag):
    corr = crypto_data['eth']['close'].corr(crypto_data['ltc']['close'].shift(lag))
    print((float(corr) ** 2) * 100)


def add_macd(df, slow_ema=26, fast_ema=12):
    df26 = df["close"].ewm(span=slow_ema, min_periods=slow_ema).mean()
    df12 = df["close"].ewm(span=fast_ema, min_periods=fast_ema).mean()
    df['MACD'] = (df12 - df26)


def add_bol(df, window=20, sd=2):
    df['Bol_upper'] = df['close'].rolling(window=window).mean() + sd * df['close'].rolling(window=window,
                                                                                           min_periods=window).std()
    df['Bol_lower'] = df['close'].rolling(window=window).mean() - sd * df['close'].rolling(window=window,
                                                                                           min_periods=window).std()
