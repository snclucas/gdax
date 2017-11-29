import pandas as pd
import time

import trading
import analysis
import gdax_data


def run(intervals, product_id="ETH-USD", history=3):
    best_bid_ask = trading.get_best_bid_ask(product_id)
    best_bid = float(best_bid_ask['bid'])

    results = []

    for int_ in intervals:
        data, start, end = gdax_data.get_data("ETH-USD", int_, 10)
        df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        analysis.add_macd(df)

        is_last_above_zero = False
        for i in range(0, history):
            print(-1-i)
            data = df.iloc[-1-i]
            if i == 0 and float(data['macd']) > 0.0:
                is_last_above_zero = True

        last_data_but_one = df.iloc[-2]
        last_data = df.iloc[-1]
        print(last_data_but_one)

        upper_bol = round(float(last_data['Bol_upper']), 2)
        lower_bol = round(float(last_data['Bol_lower']), 2)
        bol_range = upper_bol - lower_bol
        range_pc = round(((1 - (upper_bol - best_bid) / bol_range) * 100), 2)

        if range_pc > upper_limit:
            res = "SELL"
        elif range_pc < lower_limit:
            res = "BUY"
        else:
            res = "-"

        results.append(res)
        time.sleep(1)

    return results

if __name__ == '__main__':
    print(run([60, 120, 240, 600, 1200, 3600], "ETH-USD"))
