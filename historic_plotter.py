from datetime import datetime, date, time, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt
import gdax_data
import analysis
import trading

from GdaxExchangeAuth import GdaxExchangeAuth

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
    print(trading.get_best_bid_ask("ETH-USD"))

    analysis.add_macd(df)
    analysis.add_bol(df)

    fig, axes = plt.subplots(nrows=2, ncols=1)
    df.plot(y=['close', 'Bol_upper', 'Bol_lower'], ax=axes[0])
    df.plot(y=['MACD'], ax=axes[1])
    plt.show(block=False)
    return

if __name__ == '__main__':
    plot("eth", 60, 200)
