import pandas as pd

import indicators
from data import gdax_data


def name():
    return "Candlestick"


def run(interval, product_id="ETH-USD"):

    data, start, end = gdax_data.get_data(product_id, interval, 3)
    df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    indicators.check_engulfing(df)
    indicators.check_hammer(df)
    indicators.check_doji(df)

    res_string = ""
    res_score = 0
    last_data_point = df.iloc[-1]
    if bool(last_data_point['engulfing']) is True:
        res_string = res_string + "BUY (engulfing)"
        res_score = res_score + 10

    if bool(last_data_point['hammer']) is True:
        res_string = res_string + "BUY (hammer)"
        res_score = res_score + 10

    if bool(last_data_point['doji']) is True:
        res_string = res_string + "BUY (doji)"
        res_score = res_score + 10

    return {"score": res_score, "indicator": res_string}


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
    print(run(3600, "ETH-USD"))