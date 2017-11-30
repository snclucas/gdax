import pandas as pd

import indicators
import trading
from data import gdax_data


def name():
    return "Boll"


def run(interval, product_id="ETH-USD", window=20, sd=2, lower_limit=10, upper_limit=90):
    best_bid_ask = trading.get_best_bid_ask(product_id)
    best_bid = float(best_bid_ask['bid'])

    data, start, end = gdax_data.get_data(product_id, interval, window)
    df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    indicators.add_bol(df, window, sd)

    last_data = df.iloc[-1]

    upper_bol = round(float(last_data['Bol_upper']), 2)
    lower_bol = round(float(last_data['Bol_lower']), 2)
    bol_range = upper_bol - lower_bol
    range_pc = round(((1 - (upper_bol - best_bid) / bol_range) * 100), 2)

    res_string = ""
    res_score = 0

    if range_pc > upper_limit:
        res = "SELL"
        res_score = -10
    elif range_pc < lower_limit:
        res = "BUY"
        res_score = 10
    else:
        res = "-"

    return {"score": res_score, "indicator": "Boll"}

if __name__ == '__main__':
    print(run(3600, "ETH-USD"))
