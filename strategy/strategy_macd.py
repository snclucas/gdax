import time

import pandas as pd

import analysis
from data import gdax_data


def name():
    return "MACD"


def run(intervals, product_id="ETH-USD", slow_ema=26, fast_ema=12, history=3):

    results = []

    for int_ in intervals:
        data, start, end = gdax_data.get_data(product_id, int_, (slow_ema + history))
        df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        analysis.add_macd(df, slow_ema, fast_ema)

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

        if is_last_above_zero and rest_below_zero:
            res = "BUY"
        elif is_last_below_zero and rest_above_zero:
            res = "SELL"
        else:
            res = "-"

        results.append(res)
        time.sleep(1)

    return results

if __name__ == '__main__':
    print(run([60, 120, 240, 600, 1200, 3600], "ETH-USD"))
