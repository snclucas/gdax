import datetime
import os

import pytz
import requests

from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def get_data_with_bounds(product_id, granularity, start, end):
    eastern = pytz.timezone('US/Eastern')
    start = eastern.localize(start)  # .replace(tzinfo=pytz.UTC)
    end = eastern.localize(end)

    url = API_URL + 'products/' + str(product_id) + '/candles?start=' + \
          str(start.isoformat()) + '&end=' + \
          str(end.isoformat()) + '&granularity=' + str(
        granularity)

    data_result = requests.get(url, auth=auth)

    if data_result.status_code == 200:
        return data_result.json()
    else:
        print("Error: " + str(data_result.status_code))
        print(data_result.json())
        return


def get_data(product_id, granularity=3600, max_=200):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=(max_ * int(granularity)))

    return get_data_with_bounds(product_id, granularity, start, end), start, end
