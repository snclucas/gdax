import os
import pandas as pd

import gdax_data

from GdaxExchangeAuth import GdaxExchangeAuth

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


def correlation(crypto_data, lag):
    corr = crypto_data['eth']['close'].corr(crypto_data['ltc']['close'].shift(lag))
    print((float(corr)**2)*100)


def add_macd(df):
    df26 = df["close"].ewm(span=26, min_periods=26).mean()
    df12 = df["close"].ewm(span=12, min_periods=12).mean()
    df['MACD'] = (df12 - df26)


def add_bol(df):
    df['Bol_upper'] = df['close'].rolling(window=20).mean() + 2 * df['close'].rolling(window=20, min_periods=20).std()
    df['Bol_lower'] = df['close'].rolling(window=20).mean() - 2 * df['close'].rolling(window=20, min_periods=20).std()
