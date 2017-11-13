import requests
import os
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


# axes = plt.subplots(2,1)

x = np.linspace(0, (float(depth)/100.0)-increment, depth)
plt.ion()
plt.show()

# axes.ion()

for ii in range(0, 10):
    gdaxOrderBook.save(currentPrice, volume, orderBookResult.json())

    [total, asks, bids] = gdaxOrderBook.get_snapshot(',')

    total_sum = []
    running_total = 0.0
    for i in range(0, depth):
        running_total = running_total + total[i]
        total_sum.append(running_total)

    #print(total)
    #print((depth/100)-1)

    #print(x)

    plt.plot(x, total)
    plt.draw()
    plt.pause(0.05)

    # axes[0].plot(x, total, label='total')
    # axes[0].plot(x, asks, label='asks')
    # axes[0].plot(x, bids, label='bids')
    # axes[0].legend()
    #
    # axes[1].plot(x, total_sum, label='total_sum')
    # axes[1].legend()
    #
    # plt.show()

    time.sleep(2)


file = open('bids.txt', 'w')
file.write(str(gdaxOrderBook.get_snapshot(',')))
file.close()

#print(r.json())

