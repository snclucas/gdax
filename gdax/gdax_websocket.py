import _thread
import json
import os
import time
from multiprocessing import Process

import requests
import websocket
from GdaxOrderBook import GdaxOrderBook

from gdax.GdaxExchangeAuth import GdaxExchangeAuth

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
    ]
}

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend)


def save_snapshot():
    print("save_snapshot")
    [total, asks, bids] = gdaxOrderBook.get_snapshot(',')
    total_sum = []
    running_total = 0.0
    for i in range(0, depth):
        running_total = running_total + (depth - i) * total[i] / depth
        total_sum.append(running_total)
    file = open('data.txt', 'a')
    file.write(str(total_sum)+'\n')
    file.close()
    time.sleep(2)

def on_message(ws, message):
    msg_json = json.loads(message)
    if msg_json['type'] == 'l2update':
        gdaxOrderBook.update_order_book_by_websocket(message)
        print("dd")


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

    p = Process(target=save_snapshot)
    p.start()
    p.join()

    ws.on_open = on_open
    ws.run_forever()


