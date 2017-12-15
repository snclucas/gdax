import datetime
import pandas as pd

import pytz
import requests


def get_data(product, market, start_, end_, interval):
    url = 'https://api.cryptowat.ch/markets/' + market + '/' + product + '/ohlc'
    url_params = '?before=' + str(int(end_)) + '&after=' + str(int(start_)) + '&periods=' + str(interval)
    print(url + url_params)
    result = requests.get(url + url_params)
    return result.json()


def correlation(data1, data2, lag):
    return data1.corr(data2.shift(lag))


if __name__ == '__main__':
    interval = 1800
    eastern = pytz.timezone('US/Eastern')
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=30)
    start = eastern.localize(start)
    end = eastern.localize(end)

    gdax_kraken = get_data('ethusd', 'bitfinex', start.timestamp(), end.timestamp(), interval)
    gdax_eth = get_data('ethusd', 'gdax', start.timestamp(), end.timestamp(), interval)

    gdax_eth = gdax_eth['result'][str(interval)]
    gdax_kraken = gdax_kraken['result'][str(interval)]

    df_gdax_eth = pd.DataFrame(list(reversed(gdax_eth)),
                               columns=['CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume', ''])

    df_gdax_kraken = pd.DataFrame(list(reversed(gdax_kraken)),
                                  columns=['CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume', ''])

    for i in range(-5, 5):
        cor = correlation(df_gdax_eth['ClosePrice'], df_gdax_kraken['ClosePrice'], i)
        print(str(i) + " " + str(cor))
