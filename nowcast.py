import _thread
import json
import os
import time
import threading
from multiprocessing import Process

import matplotlib.pyplot as plt
import numpy as np
import requests
import websocket
from gdax.GdaxOrderBook import GdaxOrderBook as gdaxOrderBook

from gdax.GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)

subscribe_string_tosend = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"
    ],
    "channels": [
        "level2"
    ]
}

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend)


def on_message(ws, message):
    msg_json = json.loads(message)
    if msg_json['type'] == 'l2update':
        gdaxOrderBook.update_order_book_by_websocket(message)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(subscribe_string_tosend_json)



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://ws-feed.gdax.com', on_message=on_message, on_open=on_open, on_close=on_close)
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
        update_plot()