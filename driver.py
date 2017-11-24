import pandas as pd
import time

import trading
import analysis
import gdax_data

intervals = [1]

best_bid_ask = trading.get_best_bid_ask('ETH-USD')
best_bid = float(best_bid_ask['bid'])

display_str = ""

for int_ in intervals:
    data, start, end = gdax_data.get_data("ETH-USD", int_, 10)
    df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    df2 = pd.DataFrame(data, columns=['date', 'low', 'high', 'open', 'close', 'volume'])
    print(df2)
    analysis.add_macd(df)
    analysis.add_bol(df)

    last_data = df.iloc[-1]

    macd = round(float(last_data['MACD']), 2)
    upper_bol = float(last_data['Bol_upper'])
    lower_bol = float(last_data['Bol_lower'])
    bol_range = upper_bol - lower_bol
    range_pc = round(((1 - (upper_bol - best_bid) / bol_range) * 100), 2)

    print(best_bid)
    print(upper_bol)
    print(lower_bol)
    print(bol_range)
    print(range_pc)
    print("------------------")

    display_str = display_str + " " + str(range_pc) + "/" + str(macd)
    time.sleep(1)

print(display_str)


# for i in range(-5, 5):
#     analysis.correlation(data, i)

