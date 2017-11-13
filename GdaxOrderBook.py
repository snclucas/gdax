import datetime
import json
import collections


# Create custom authentication for Exchange
class GdaxOrderBook():
    def __init__(self, current_price, depth, increment):
        self.depth = depth
        self.increment = increment
        self.date_time_stamp = ""
        self.current_price = current_price
        self.volume = 0
        self.order_book = {'asks': collections.OrderedDict(), 'bids': collections.OrderedDict()}

        self.__create_order_book_dict__(self.depth, self.current_price, self.increment)
        d=4

        # poll to get fu,l order book here first

    def update_order_book_by_websocket(self, update):
        update_json = json.loads(update)
        changes = update_json['changes']
        buy_or_sell = changes[0][0]
        price = changes[0][1]
        size = changes[0][2]
        self.__update_order_book__(buy_or_sell, price, size)

    def save(self, current_price, volume, json_order_book):
        self.date_time_stamp = str(datetime.datetime.now())
        self.current_price = current_price
        self.volume = volume

        reversed_asks = list(reversed(json_order_book['asks'][:self.depth]))

        for x in range(0, self.depth):
            price = reversed_asks[x][0]
            size = reversed_asks[x][1]
            self.__update_order_book__('asks', price, size)

        for x in range(0, self.depth):
            price = json_order_book['bids'][x][0]
            size = json_order_book['bids'][x][1]
            self.__update_order_book__('bids', price, size)

        f=4

    def get_snapshot(self, delim=','):
        ask_string = ""
        bid_string = ""
        for i in range(0, self.depth):
            ask_key = "{0:.2f}".format(round(float(self.current_price) + i * float(self.increment), 2))
            bid_key = "{0:.2f}".format(round(float(self.current_price) - i * float(self.increment), 2))
            ask_string = ask_string + str(self.order_book['asks'][ask_key]) + delim
            bid_string = bid_string + str(self.order_book['bids'][bid_key]) + delim
        print(bid_string)

    def json(self):
        return json.dumps(self.__dict__)

    def __update_order_book__(self, type, price, size):
        if price in self.order_book[type]:
            self.order_book[type][price] = size

    def __create_order_book_dict__(self, depth, current_price, increment):
        for i in range(0, depth):
            ask_key = "{0:.2f}".format(round(float(current_price)+i*float(increment), 2))
            bid_key = "{0:.2f}".format(round(float(current_price)-i*float(increment), 2))
            self.order_book['asks'][ask_key] = 0.0
            self.order_book['bids'][bid_key] = 0.0
