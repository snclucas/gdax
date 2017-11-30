import time

import pandas as pd

import indicators
import trading
from data import gdax_data

intervals = [60, 300, 600, 1200, 3600]

best_bid_ask = trading.get_best_bid_ask('ETH-USD')
best_bid = float(best_bid_ask['bid'])

display_str = ""

for int_ in intervals:
    data, start, end = gdax_data.get_data("ETH-USD", int_, 200)
    df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    indicators.add_macd(df)
    indicators.add_bol(df)

    last_data = df.iloc[-1]

    macd = round(float(last_data['MACD']), 2)
    upper_bol = round(float(last_data['Bol_upper']), 2)
    lower_bol = round(float(last_data['Bol_lower']), 2)
    bol_range = upper_bol - lower_bol
    range_pc = round(((1 - (upper_bol - best_bid) / bol_range) * 100), 2)

    print(str(int_) + " " + str(range_pc) + "/" + str(macd) + "  ["
          + str(lower_bol) + " <- " + str(best_bid) + " -> " + str(upper_bol) + "]")
    time.sleep(1)
