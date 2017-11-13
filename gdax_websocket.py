import websocket
import _thread
import json
import os
import requests
import matplotlib.pyplot as plt
import numpy as np
import time

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

depth = 200
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
        "heartbeat",
        {
            "name": "ticker",
            "product_ids": [
                "ETH-USD"
            ]
        },
    ]
}

subscribe_string_tosend2 = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"
    ],
    "channels": [
        "level2",
    ]
}

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend2)


x = np.linspace(0, (float(depth) / 100.0) - increment, depth)
x = np.linspace(0, depth-1, depth)
plt.ion()
plt.show()
p = plt.plot()

def on_message(ws, message):
    msg_json = json.loads(message)
    if msg_json['type'] == 'l2update':
        gdaxOrderBook.update_order_book_by_websocket(message)
        total = []
        [total, asks, bids] = gdaxOrderBook.get_snapshot(',')
        total_sum = []
        running_total = 0.0
        for i in range(0, depth):
            running_total = running_total + total[i]
            total_sum.append(running_total)

        # print(running_total)
        plt.cla()
        plt.plot(x, total_sum)
        plt.draw()
        plt.pause(0.05)
        # time.sleep(1)
        # print(total)
    # print(message)



def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run():
        ws.send(subscribe_string_tosend_json)

    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://ws-feed.gdax.com',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
