import websocket
import threading
import json
import requests, os, time
import matplotlib.pyplot as plt
import numpy as np

from GdaxExchangeAuth import GdaxExchangeAuth
from GdaxOrderBook import GdaxOrderBook


API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)

currentPriceResult = requests.get(API_URL + 'products/ETH-USD/ticker', auth=auth)
currentPrice = currentPriceResult.json()['price']
volume = currentPriceResult.json()['volume']

orderBookResult = requests.get(API_URL + 'products/ETH-USD/book?level=3', auth=auth)

depth = 2000
increment=0.01
gdaxOrderBook = GdaxOrderBook(current_price=currentPrice, depth=depth, increment=increment)
gdaxOrderBook.save(currentPrice, volume, orderBookResult.json())


subscribe_string_tosend = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"
    ],
    "channels": [
        "level2",
    ]
}

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend)


def on_message(ws, message):
    msg_json = json.loads(message)
    if msg_json['type'] == 'l2update':
        gdaxOrderBook.update_order_book_by_websocket(message)


def on_close(ws):
    print ("### closed ###")


def on_open(ws):
    ws.send(subscribe_string_tosend_json)

x = np.linspace(0, (float(depth) / 100.0) - increment, depth)
plt.ion()
plt.show()
plt.plot()


def update_plot():
    print("updating plot")
    [total, asks, bids] = gdaxOrderBook.get_snapshot(',')
    total_sum = []
    running_total = 0.0
    for i in range(0, depth):
        running_total = running_total + (depth - i) * total[i] / depth
        total_sum.append(running_total)

    plt.cla()
    plt.plot(x, total_sum)
    plt.draw()
    plt.pause(0.05)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://ws-feed.gdax.com', on_message = on_message, on_open = on_open, on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
        time.sleep(1)
        conn_timeout -= 1

    msg_counter = 0
    while ws.sock.connected:
        time.sleep(1)
        print("plot")
        update_plot()
