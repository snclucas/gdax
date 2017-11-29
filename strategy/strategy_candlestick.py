import time

import pandas as pd

import analysis
from data import gdax_data


def name():
    return "Candlestick"


def run(intervals, product_id="ETH-USD"):
    results = []

    for int_ in intervals:
        data, start, end = gdax_data.get_data(product_id, int_, 200)
        df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        df = df.astype('float')

        analysis.check_engulfing(df)

        # print(df)


def check_engulfing(current_candle, last_candle1):
    if candle_color(current_candle) == 'white' and candle_color(last_candle1) == 'black':
        if current_candle['open'] > last_candle1['open'] and current_candle['close'] < last_candle1['close']:
            if current_candle['high'] > last_candle1['high'] and current_candle['low'] < last_candle1['low']:
                return True
    return False


def check_hammer(cur_candle):
    if candle_color(cur_candle) == 'white':
        if cur_candle['close'] >= cur_candle['high']:
            if (cur_candle['open'] - cur_candle['low']) > 2*(cur_candle['close'] - cur_candle['open']):
                return True
    return False


def check_doji(cur_candle):
    if cur_candle['high'] > cur_candle['close']:
        if cur_candle['low'] < cur_candle['open']:
            if cur_candle['close'] / cur_candle['open'] < 1.001:
                return True
    return False


def candle_color(candle):
    if candle['close'] >= candle['open']:
        return 'white'
    else:
        return 'black'


if __name__ == '__main__':
    print(run([3600], "ETH-USD"))