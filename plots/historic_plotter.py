import os

import matplotlib.pyplot as plt
import pandas as pd

import analysis
import trading
from data import gdax_data
from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def plot(product_id, granularity=60, max=200):
    crypto_id = product_id.upper()
    product_id = crypto_id + '-USD'
    gdax_data_, start, end = gdax_data.get_data(product_id, granularity, max)

    df = pd.DataFrame(list(reversed(gdax_data_)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    print(trading.get_best_bid_ask(product_id))

    analysis.add_macd(df)
    analysis.add_bol(df)

    fig, axes = plt.subplots(nrows=2, ncols=1)
    df.plot(y=['close', 'Bol_upper', 'Bol_lower'], ax=axes[0])
    df.plot(y=['MACD'], ax=axes[1])
    plt.show(block=False)
    return

if __name__ == '__main__':
    plot("eth", 3600, 200)
