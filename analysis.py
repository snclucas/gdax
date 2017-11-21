import requests
import os
import json
import pandas as pd

import data

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def correlation(lag):
    eth_data = data.get_data("ETH-USD")
    btc_data = data.get_data("BTC-USD")
    ltc_data = data.get_data("LTC-USD")

    eth_df = pd.DataFrame(list(reversed(eth_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    btc_df = pd.DataFrame(list(reversed(btc_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    ltc_df = pd.DataFrame(list(reversed(ltc_data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    corr = eth_df['close'].corr(ltc_df['close'].shift(lag))
    print((float(corr)**2)*100)

for i in range(-5, 5):
    correlation(i)
