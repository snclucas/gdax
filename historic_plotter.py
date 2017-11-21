import requests
import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def get_data(product_id, granularity=3600, max=200):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=(max * granularity))
    url = API_URL + 'products/' + str(
        product_id) + '/candles?start=' + start.isoformat() + '&end=' + end.isoformat() + '&granularity=' + str(
        granularity)
    data_result = requests.get(url, auth=auth)
    return data_result.json()


data = get_data('ETH-USD')
df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
df['Bol_upper'] = df['close'].rolling(window=20).mean() + 2 * df['close'].rolling(window=20, min_periods=20).std()
df['Bol_lower'] = df['close'].rolling(window=20).mean() - 2 * df['close'].rolling(window=20, min_periods=20).std()

df['26 ema'] = pd.ewma(df["close"], span=26)
df['12 ema'] = pd.ewma(df["close"], span=12)
df['MACD'] = (df['12 ema'] - df['26 ema'])

# fig, axes = plt.subplots(nrows=2, ncols=2)
df.plot(y=['close', 'Bol_upper', 'Bol_lower'])
df.plot(y=['MACD'])

plt.show()
