import pandas as pd
import numpy as np
import datetime
import pytz
import matplotlib.pyplot as plt
import time, math

from data import gdax_data
import indicators


# 1hr 3600 24
# 0.5hr 1800 48
# 15 min 900 96
# 10 min 600 144

def make_histogram(product_id, interval, num):

    hist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    num_bins = int(int(24*3600) / int(interval))
    y = np.arange(num_bins)
    y_date = np.zeros(num_bins)
    hist = np.zeros(num_bins)

    arr = np.array([datetime.datetime.now() + datetime.timedelta(seconds=i*interval) for i in range(num_bins)])

    df_total = pd.DataFrame()

    for i in range(0, num):
        print(i)
        end = datetime.datetime.now().replace(microsecond=0, second=0, minute=0) - datetime.timedelta(days=1*i)
        start = end - datetime.timedelta(hours=24)
        print("start " + str(start))
        print("end " + str(end))

        data = gdax_data.get_data_with_bounds(product_id, interval, start, end)
        df = pd.DataFrame(list(data), columns=['date', 'low', 'high', 'open', 'close', 'volume'])
        convert_date(df)
        df['diff'] = df['close'].diff()
        indicators.add_sd("sd", df)

        df_total = df_total.append(df)
        time.sleep(2)

    for index, row in df_total.iterrows():
        index = int((int(row['date'].hour) * 3600 + int(row['date'].minute * 60) + int(row['date'].second)) / interval)
        arr[index] = row['date']

        close_price_diff = row['diff']

        if not np.isnan(close_price_diff):
            if close_price_diff >= row['sd']:
                hist[index] = hist[index] + 1

        print(str(index) + " " + str(close_price_diff))
        #if not np.isnan(close_price_diff):
        #    hist[index] = hist[index] + close_price_diff

    hist = [x / num for x in hist]
    plt.bar(y, hist)
    plt.show()


def convert_date(df):
    df['date'] = df.apply(lambda x:
                          convert_date_func(x['date']), axis=1)


def convert_date_func(date):
    eastern = pytz.timezone('US/Eastern')
    return eastern.localize(datetime.datetime.utcfromtimestamp(date))


if __name__ == '__main__':
    make_histogram("ETH-USD", 600, 50)
