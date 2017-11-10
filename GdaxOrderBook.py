import datetime
import json


# Create custom authentication for Exchange
class GdaxOrderBook():
    def __init__(self, width):
        self.width = width

        self.date_time_stamp = ""
        self.current_price = 0
        self.volume = 0
        self.asks = []
        self.bids = []
        self.order_book = {'asks': {}, 'bids': {}}
poll to get fu,l order book here first
    def update_order_book(self, update):
        update_json = json.loads(update)
        changes = update_json['changes']
        buy_or_sell = update_json['changes'][0][0]
        price = update_json['changes'][0][1]
        size = update_json['changes'][0][2]
        if buy_or_sell == 'buy':
            self.order_book['asks'][price] = size
        print(len(self.order_book['asks']))

    def save(self, current_price, volume, json_order_book):
        self.date_time_stamp = str(datetime.datetime.now())
        self.current_price = current_price
        self.volume = volume

        len(json_order_book['asks'])

        reversed_asks = list(reversed(json_order_book['asks'][:self.width]))

        for x in range(0, self.width):
            # self.prices.append(reversed_asks[x][0])
            self.asks.append([reversed_asks[x][0], reversed_asks[x][1]])
            # self.amounts.append(reversed_asks[x][1])
            # print(reversed_asks[x])  # low to high

        for x in range(0, self.width):
            # self.prices.append(json_order_book['bids'][x][0])
            # self.amounts.append(json_order_book['bids'][x][1])
            self.bids.append([json_order_book['bids'][x][0], json_order_book['bids'][x][1]])
            # print(self.order_book['bids'][x])  # high to low

    def json(self):
        return json.dumps(self.__dict__)
