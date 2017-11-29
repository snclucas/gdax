import json
import os
import sched
import time

import requests

from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


def limit_order(amount, side, product):
    order_book_result = requests.get(API_URL + 'products/'+product+'/book?level=1', auth=auth)
    json_order_book = order_book_result.json()
    best_ask = json_order_book['asks'][0]
    best_bid = json_order_book['bids'][0]

    limit_price = best_bid[0]

    order = {
        'size': str(amount),
        'price': str(float(limit_price)-1),
        'side': side,
        'product_id': product,
    }
    print(order)
    print(str(json.loads(json.dumps(order))))
    r = requests.post(API_URL + 'orders', json=order, auth=auth)
    print(r.json())


s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    s.enter(60, 1, do_something, (sc,))






# Get accounts
# r = requests.get(API_URL + 'orders?status=open', auth=auth)
#
# orders = r.json()
# for order in orders:
#     if order['status'] == 'open':
#         order_price = order['price']


if __name__ == "__main__":
    trail_pc = 5.0 / 100

    limit_order(1, 'buy', 'ETH-USD')

    s.enter(60, 1, do_something, (s,))
    s.run()