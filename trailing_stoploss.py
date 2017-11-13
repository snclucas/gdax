import requests
import os
import sched, time

from GdaxExchangeAuth import GdaxExchangeAuth
from GdaxOrderBook import GdaxOrderBook

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)

trail_pc = 5.0/100


s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    s.enter(60, 1, do_something, (sc,))

s.enter(60, 1, do_something, (s,))
s.run()


currentPriceResult = requests.get(API_URL + 'products/ETH-USD/ticker', auth=auth)
currentPrice = currentPriceResult.json()['price']

# Get accounts
r = requests.get(API_URL + 'orders?status=open', auth=auth)

orders = r.json()
for order in orders:
    if order['status'] == 'open':
        order_price = order['price']




# [{"id": "a1b2c3d4", "balance":...

# Place an order
order = {
    'size': 1.0,
    'price': 1.0,
    'side': 'buy',
    'product_id': 'BTC-USD',
}
#r = requests.post(api_url + 'orders', json=order, auth=auth)
#print(r.json())
# {"id": "0428b97b-bec1-429e-a94c-59992926778d"}