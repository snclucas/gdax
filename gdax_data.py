import requests
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import ta

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def get_data(product_id, granularity=3600, max=200):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=(max * int(granularity)))

    eee = end - datetime.timedelta(seconds=(1511534784))
    print(eee)

    print(start)
    print(end)
    url = API_URL + 'products/' + str(
        product_id) + '/candles?start=' + start.isoformat() + '&end=' + end.isoformat() + '&granularity=' + str(
        granularity)
    data_result = requests.get(url, auth=auth)
    if data_result.status_code == 200:
        return data_result.json(), start, end
    else:
        print("Error: " + data_result.status_code)
        print(data_result.json())
        return
