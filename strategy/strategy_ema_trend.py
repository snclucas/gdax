import pandas as pd
import numpy as np

import indicators
from data import gdax_data


def name():
    return "EMA Trend"


def run(intervals, product_id="ETH-USD", window=19, history=5):
    results = []
    for interval in intervals:
        data, start, end = gdax_data.get_data(product_id, interval, (window + history))

        df = pd.DataFrame(list(reversed(data)), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        indicators.add_ema('mean', df, window)

        df = df.dropna(how='any').reset_index(drop=True)
        x = list(range(1, history+1))
        y = df['mean'].values[-history:]
        z = np.polyfit(x=x, y=y, deg=1)
        p = np.poly1d(z)
        results.append({"interval": interval, "score": z[0], "indicator": "Slope"})
        print(str(interval) + " " + str(z[0]))
    return results

if __name__ == '__main__':
    #print(run([60], "ETH-USD"))
    run([60, 300, 900, 3600, 6*3600, 24*3600], "ETH-USD")
