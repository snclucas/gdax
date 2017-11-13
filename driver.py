import requests
import os

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
gdaxOrderBook = GdaxOrderBook(current_price=currentPrice, depth=1000, increment=0.01)
gdaxOrderBook.save(currentPrice, volume, orderBookResult.json())

print(gdaxOrderBook.json())

gdaxOrderBook.get_snapshot(',')

#print(r.json())

