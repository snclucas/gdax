import json

# Create custom authentication for Exchange
class GdaxOrderBook:
    def __init__(self, current_price, volume, json_order_book):
        self.order_book = json_order_book
        print((self.order_book['asks']))
