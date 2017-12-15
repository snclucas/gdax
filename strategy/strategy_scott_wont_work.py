import pandas as pd
import numpy as np

import indicators
from data import gdax_data


def name():
    return "EMA Trend"


def run(intervals, product_id="ETH-USD", window=3):
    is_reversed = True
    for interval in intervals:
        data, start, end = gdax_data.get_data(product_id, interval, 200)
        if is_reversed:
            df = pd.DataFrame(list(reversed(data)),
                              columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        else:
            df = pd.DataFrame(list(data),
                              columns=['date', 'low', 'high', 'open', 'close', 'volume'])

        if not is_reversed:
            df['temp'] = df['open']
            df['open'] = df['close']
            df['close'] = df['temp']

        indicators.check_color(df)

        have_position = False

        num_green = 0
        fiat_start_balance = 1000.0
        fiat_balance = fiat_start_balance
        eth_balance = 0.0
        close_price = 0.0

        for index, row in df.iterrows():
            close_price = row['close']

            if row['color'] == 'green':
                num_green = num_green + 1

            if have_position and row['color'] == 'green':
                print("HOLD SHIZZLE " + str(close_price))

            if not have_position and num_green == 3:
                eth_balance = fiat_balance / close_price
                fiat_balance = 0.0
                have_position = True
                num_green = 0
                print("BUY " + str(close_price))

            if have_position and row['color'] == 'red':
                fiat_balance = eth_balance * close_price
                eth_balance = 0.0
                have_position = False
                num_green = 0
                print("SELL " + str(close_price))

        print(str(fiat_balance) + " " + str(close_price * eth_balance))


if __name__ == '__main__':
    run([600], "ETH-USD")
