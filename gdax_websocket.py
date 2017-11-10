import websocket
import _thread
import json

from GdaxOrderBook import GdaxOrderBook

gdaxOrderBook = GdaxOrderBook(1000)

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


def on_message(ws, message):
    gdaxOrderBook.update_order_book(message)
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
