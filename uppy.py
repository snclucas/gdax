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

depth = 500
increment=0.01
gdaxOrderBook = GdaxOrderBook(current_price=currentPrice, depth=depth, increment=increment)
gdaxOrderBook.save(currentPrice, volume, orderBookResult.json(), level=3)


subscribe_string_tosend = {
    "type": "subscribe",
    "product_ids": [
        "ETH-USD"
    ],
    "channels": [
        "level2",
        "ticker"
    ]
}

subscribe_string_tosend_json = json.dumps(subscribe_string_tosend)

old_price = 0.0
current_price = 0.0
price_delta = 0.0

def on_message(ws, message):
    msg_json = json.loads(message)
    if msg_json['type'] == 'l2update':
        gdaxOrderBook.update_order_book_by_websocket(message)
    if msg_json['type'] == 'ticker':
        # {"type":"ticker","sequence":1476074535,"product_id":"ETH-USD","price":"330.71000000","open_24h":"314.92000000",
        # "volume_24h":"201521.01137615","low_24h":"330.71000000","high_24h":"336.91000000","volume_30d":"3428726.29510153",
        # "best_bid":"330.71","best_ask":"330.9","side":"sell","time":"2017-11-14T15:52:24.045000Z","trade_id":15293634,
        # "last_size":"11.58130000"}
        global old_price
        global current_price
        global price_delta
        old_price = current_price
        current_price = msg_json['price']
        price_delta = float(current_price) - float(old_price)

def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(subscribe_string_tosend_json)

x = np.linspace(0, (float(depth) / 100.0) - increment, depth)
plt.ion()
plt.show()
plt.plot()


def update_plot():
    print("updating plot")
    [total, asks, bids] = gdaxOrderBook.get_snapshot(',')
    print(gdaxOrderBook.get_statistics())
    total_sum = []
    running_total = 0.0
    for i in range(0, depth):
        running_total = running_total + (depth - i) * total[i] / depth
        total_sum.append(running_total)

    # plt.subplot(3, 1, 1)
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=1)
    ax1.cla()
    ax1.plot(x, asks, label='asks')
    ax1.plot(x, bids, label='bids')
    ax1.legend()

    # plt.subplot(3, 1, 2)
    ax2 = plt.subplot2grid((2, 3), (1, 0), colspan=1)
    ax2.cla()
    ax2.plot(x, total, label='total')
    ax2.legend()

    # plt.subplot(3, 1, 3)
    ax3 = plt.subplot2grid((2, 3), (0, 1), rowspan=2)
    ax3.cla()
    ax3.plot(x, total_sum, label='sum(ask-bid)')
    ax3.legend()

    ax3 = plt.subplot2grid((2, 3), (0, 2), rowspan=2)
    if float(price_delta) > 0:
        ax3.arrow(0.5, 0.25, 0.0, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
    elif float(price_delta) < 0:
        ax3.arrow(0.5, 0.75, 0.0, -0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
    else:
        ax3.arrow(0.25, 0.5, 0.75, 0.0, head_width=0.05, head_length=0.1, fc='k', ec='k')

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
        update_plot()
