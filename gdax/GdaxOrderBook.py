import datetime
import json
import collections


# Create custom authentication for Exchange
class GdaxOrderBook:
    def __init__(self, current_price, depth, increment):
        self.depth = depth
        self.increment = increment
        self.date_time_stamp = ""
        self.current_price = current_price
        self.volume = 0
        self.lowest_ask_key = 0
        self.highest_ask_key = 0
        self.lowest_bid_key = 0
        self.highest_bid_key = 0

        self.stats = {'asks': {}, 'bids': {}}
        self.ask_count = 0
        self.bid_count = 0
        self.ask_size = 0
        self.bid_size = 0

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

        '''
        E.g. current price 300.00
        asks: 300.00, 300.01 -> higher
        bids: 300.00, 299.99 -> lower

        We need to list:
        reversed asks , current price, bids
        '''
    def get_snapshot(self, delim=','):
        # bids = collections.OrderedDict(reversed(list(self.order_book['bids'].items())))
        ask_total = 0.0
        bid_total = 0.0
        ask_arr = []
        bid_arr = []
        total_arr = []

        for i in range(0, self.depth):
            ask_key = self.__get_key__(i, self.current_price, 'ask')
            bid_key = self.__get_key__(i, self.current_price, 'bid')
            ask_total = ask_total + float(self.order_book['asks'][ask_key])
            bid_total = bid_total + float(self.order_book['bids'][bid_key])
            ask_arr.append(ask_total)
            bid_arr.append(bid_total)
            total_arr.append(ask_total - bid_total)
        return total_arr, ask_arr, bid_arr

    def get_statistics(self):
        return_json = {
            "ask_count": self.ask_count,
            "bid_count": self.bid_count,
            "bid_size": self.bid_size,
            "ask_size": self.ask_size
        }
        self.ask_count = 0
        self.bid_count = 0
        self.bid_size = 0
        self.ask_size = 0
        return return_json

    def json(self):
        return json.dumps(self.__dict__)

    def __update_order_book__(self, type_in, price_in, size_in):
        if type_in == 'buy':
            type_in = 'bids'
            self.bid_count = int(self.bid_count) + 1
            self.bid_size = float(self.bid_size) + float(size_in)

        if type_in == 'sell':
            type_in = 'asks'
            self.ask_count = int(self.ask_count) + 1
            self.ask_size = float(self.ask_size) + float(size_in)

        key = self.__get_key__(0, price_in, type_in)
        if key in self.order_book[type_in]:
            self.order_book[type_in][key] = size_in

    def __create_order_book_dict__(self, depth, current_price, increment):
        for i in range(0, depth):
            ask_key = self.__get_key__(i, current_price, 'ask')
            bid_key = self.__get_key__(i, current_price, 'bid')
            self.order_book['asks'][ask_key] = 0.0
            self.order_book['bids'][bid_key] = 0.0

    def __get_key__(self, i, offset, ask_or_bid):
        inc_op = 1 if ask_or_bid == 'ask' else -1
        return "{0:.2f}".format(round(float(offset) + inc_op * float(i) * float(self.increment), 2))
