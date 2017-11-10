

# Create custom authentication for Exchange
class GdaxOrderBook:
    def __init__(self, current_price, volume, json_order_book):
        self.width = 100
        self.price = current_price
        self.volume = volume
        self.order_book = json_order_book

        self.prices = []
        self.amounts = []

        len(self.order_book['asks'])

        reversed_asks = list(reversed(self.order_book['asks'][:self.width]))

        for x in range(0, self.width):
            self.prices.append(reversed_asks[x][0])
            self.amounts.append(reversed_asks[x][1])
            print(reversed_asks[x])  # low to high

        print("---------------------")
        print(current_price)
        print("---------------------")

        for x in range(0, self.width):
            self.prices.append(self.order_book['bids'][x][0])
            self.amounts.append(self.order_book['bids'][x][1])
            print(self.order_book['bids'][x])  # high to low
