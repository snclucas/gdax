import pandas as pd

import indicators
from data import gdax_data


def name():
    return "MACD"


def run(interval, product_id="ETH-USD", slow_ema=26, fast_ema=12, history=3):

    data, start, end = gdax_data.get_data(product_id, interval, (slow_ema + history))
    df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    indicators.add_macd(df, slow_ema, fast_ema)

    is_last_above_zero = False
    is_last_below_zero = False
    rest_above_zero = False
    rest_below_zero = False
    for i in range(0, history):
        data = df.iloc[-1-i]

        if i == 0:
            if float(data['MACD']) > 0.0:
                is_last_above_zero = True
            else:
                is_last_below_zero = True

        if i != 0:
            if float(data['MACD']) > 0.0:
                rest_above_zero = True
            else:
                rest_below_zero = True
                break

    res_string = ""
    res_score = 0

    if is_last_above_zero and rest_below_zero:
        res = "BUY"
        res_score = 10
    elif is_last_below_zero and rest_above_zero:
        res = "SELL"
        res_score = -10
    else:
        res = "-"

    return {"score": res_score, "indicator": "MACD"}

if __name__ == '__main__':
    print(run([60, 120, 240, 600, 1200, 3600], "ETH-USD"))
