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
    start = end - datetime.timedelta(seconds=(max*granularity))
    url = API_URL + 'products/' + str(product_id) + '/candles?start='+start.isoformat()+'&end='+end.isoformat()+'&granularity='+str(granularity)
    data_result = requests.get(url, auth=auth)
    return data_result.json()

data = get_data('ETH-USD')
df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
df['Bol_upper'] = df['close'].rolling(window=20).mean() + 2 * df['close'].rolling(window=20, min_periods=20).std()
df['Bol_lower'] = df['close'].rolling(window=20).mean() - 2 * df['close'].rolling(window=20, min_periods=20).std()

df.plot(y=['close', 'Bol_upper', 'Bol_lower'], use_index=True)
plt.show()


# data_ext.all_stock_df['Date'] = pandas.to_datetime(data_ext.all_stock_df['Date'])
# temp_data_set = data_ext.all_stock_df.sort('Date', ascending=True)  # sort to calculate the rolling mean
#
# temp_data_set['20d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20)
# temp_data_set['50d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=50)
# temp_data_set['Bol_upper'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) + 2 * pandas.rolling_std(
#     temp_data_set['Adj Close'], 20, min_periods=20)
# temp_data_set['Bol_lower'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) - 2 * pandas.rolling_std(
#     temp_data_set['Adj Close'], 20, min_periods=20)
# temp_data_set['Bol_BW'] = ((temp_data_set['Bol_upper'] - temp_data_set['Bol_lower']) / temp_data_set['20d_ma']) * 100
# temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(temp_data_set['Bol_BW'], window=50)  # cant get the 200 daa
# temp_data_set['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')  ##?? ,may not be good
# temp_data_set['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
# temp_data_set['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)
# data_ext.all_stock_df = temp_data_set.sort('Date', ascending=False)  # revese back to original
#
# data_ext.all_stock_df.plot(x='Date', y=['Adj Close', '20d_ma', '50d_ma', 'Bol_upper', 'Bol_lower'])
# data_ext.all_stock_df.plot(x='Date', y=['Bol_BW', 'Bol_BW_200MA'])
# plt.show()