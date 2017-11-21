import requests
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import data

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def plot(product_id, granularity=60, max=200):
    crypto_id = product_id.upper()
    product_id = crypto_id + '-USD'
    gdax_data = data.get_data(product_id, granularity, max)
    df = pd.DataFrame(list(reversed(gdax_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    df['Bol_upper'] = df['close'].rolling(window=20).mean() + 2 * df['close'].rolling(window=20, min_periods=20).std()
    df['Bol_lower'] = df['close'].rolling(window=20).mean() - 2 * df['close'].rolling(window=20, min_periods=20).std()

    df['26 ema'] = df["close"].ewm(span=26, min_periods=26).mean()
    df['12 ema'] = df["close"].ewm(span=12, min_periods=12).mean()
    df['MACD'] = (df['12 ema'] - df['26 ema'])


    fig, axes = plt.subplots(nrows=2, ncols=1)
    df.plot(y=['close', 'Bol_upper', 'Bol_lower'], ax=axes[0])
    df.plot(y=['MACD'], ax=axes[1])
    plt.show(block=False)
    return

