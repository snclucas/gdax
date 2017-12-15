import json
import os
import math

import pandas as pd

from data import gdax_data
from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def run(product_id="ETH-USD"):
    trade_window = float(600)
    max_points = float(200)
    window = 50

    data_1min, start, end = gdax_data.get_data(product_id, trade_window/max_points, max_points)
    df_data_1min = pd.DataFrame(list(reversed(data_1min)),
                                    columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    data_5min, start, end = gdax_data.get_data(product_id, trade_window / max_points, max_points)
    df_data_5min = pd.DataFrame(list(reversed(data_5min)),
                                columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    data_10min, start, end = gdax_data.get_data(product_id, trade_window, max_points)
    df_data_10min = pd.DataFrame(list(reversed(data_10min)),
                                     columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    df_data_1min['std'] = df_data_1min['close'].rolling(window=window, min_periods=window).std()
    df_data_5min['mean'] = df_data_5min['close'].rolling(window=window, min_periods=window).mean()

    sd = df_data_10min['std'].iloc[-2] # cannot predict future
    mean = df_data_10min['mean'].iloc[-2]  # cannot predict future

    print(sd)
    print(df_data_10min)

    start_price = df_data_1min.iloc[0]['close']
    last_price = df_data_1min.iloc[-1]['close']

    sd_pc = sd / start_price
    print(sd_pc)

    val = 400
    prob = (1/(sd*math.sqrt(2*math.pi))) * math.pow(((val-mean)/sd), 2)
    print(prob)

    take_profit_pc_arr = [0.001, 0.002, 0.003, 0.004]
    stop_loss_pc_arr = [0.001, 0.002, 0.003, 0.004]

    fiat_start_balance = 1000.0
    stop_loss_price = 0.0
    take_profit_price = 0.0

    print(str(start_price) + " " + str(last_price))

    for stop_loss_pc in stop_loss_pc_arr:
        for take_profit_pc in take_profit_pc_arr:
            fiat_start_balance = 1000.0
            fiat_balance = fiat_start_balance
            eth_balance = 0.0
            have_position = False
            for index, row in df_data_1min.iterrows():
                close_price = row['close']
                if not have_position:
                    eth_balance = fiat_balance / close_price
                    fiat_balance = 0.0
                    stop_loss_price = close_price * (1 - stop_loss_pc)
                    take_profit_price = close_price * (1 + take_profit_pc)
                    have_position = True

                if close_price <= stop_loss_price or close_price >= take_profit_price:
                    fiat_balance = eth_balance * close_price
                    eth_balance = 0.0
                    have_position = False

            if have_position:
                fiat_balance = eth_balance * last_price

            print("TP(%) " + str(take_profit_pc) + " SL(%) " + str(stop_loss_pc) + " FIAT " +
                  str(fiat_balance) + " ETH " + str(eth_balance))

    boring_shitty_way = (fiat_start_balance / start_price) * last_price
    print("boring_shitty_way " + str(boring_shitty_way))


if __name__ == '__main__':
    run("ETH-USD")
