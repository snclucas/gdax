import requests
import os
import json

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)

safety = True

def get_account_available(currency):
    account_result = requests.get(API_URL + 'accounts', auth=auth)
    account_result_json = account_result.json()
    for account in account_result_json:
        if account['currency'] == currency:
            return account['available']


def get_all_orders():
    orders_result = requests.get(API_URL + 'orders?status=open', auth=auth)
    orders_result_json = orders_result.json()
    return orders_result_json


def get_orders(side='all', product_id='eth'):
    orders_result = requests.get(API_URL + 'orders?status=open', auth=auth)
    orders_result_json = orders_result.json()

    for order in orders_result_json:
        if side == 'all' and order['product_id'] == product_id:
            return order
        elif order['product_id'] == product_id and order['side'] == side:
            return order
    return None


def update_order_price(product_id, new_price):
    order = get_orders(product_id)
    best = __get_best_bid_ask__(product_id)

    if order is None:
        print("No open order found")
        return

    order_id = order['id']
    order_price = order['price']
    order_side = order['side']
    order_size = order['size']
    order_product = order['product_id']

    if order_side == 'buy':
        if new_price > order_price:
            print("Error: Buy price above best bid")
            return
    if order_side == 'sell':
        if new_price > order_price:
            print("Error: Sell price below best ask")
            return

    cancel_order(order_id)
    limit_order(order_size, order_side, order_product)


def cancel_order(order_id):
    order_delete_result = requests.delete(API_URL + 'order/'+order_id, auth=auth)
    return order_delete_result.json()


def cancel_order(side, product_id):
    side = side.lower()
    crypto_id = product_id.upper()
    product_id = crypto_id + '-USD'
    print(crypto_id)
    if side.lower() == 'all' and crypto_id.lower() == 'all':
        cancel_result = requests.delete(API_URL + 'orders', auth=auth)
        return cancel_result.json()

    orders = get_orders(side, product_id)
    if orders is None:
        print("No open order found")
        return
    else:
        for order in orders:
            requests.delete(API_URL + 'order/'+order['id'], auth=auth)
        return "Orders cancelled"


def limit_order(amount, side, product_id, price=-1):
    crypto_id = product_id.upper()
    product_id = crypto_id+'-USD'
    if side != 'buy' and side != 'sell':
        print("You need to buy or sell")
        return

    if product_id != "ETH-USD" and product_id != "BTC-USD" and product_id != "LTC-USD":
        print("Product not found")
        return

    best = __get_best_bid_ask__(product_id)

    crypto_amount = float(amount)

    if float(price) > 0:
        limit_price = float(price)
        if side == 'buy':
            if limit_price > float(best['bid']):
                print("Error: Buy price above best bid")
                return
        if side == 'sell':
            if limit_price < float(best['ask']):
                print("Error: Sell price below best ask")
                return
    else:
        if side == 'buy':
            limit_price = float(best['bid'])
            if float(amount) < 0:
                usd = float(get_account_available('USD'))
                crypto_amount = usd / limit_price
        else:
            limit_price = float(best['ask'])
            if float(amount) < 0:
                crypto = float(get_account_available(crypto_id))
                crypto_amount = crypto
                if crypto_amount == 0:
                    print("You have no {0} to sell".format(crypto_id))
                    return

    if safety is True:
        print("Safety is on")
        if side == 'buy':
            limit_price = limit_price - 1
        elif side == 'sell':
            limit_price = limit_price + 1

    crypto_amount = round(crypto_amount, 6)

    order = {
        'size': str(crypto_amount),
        'price': str(float(limit_price)),
        'side': side,
        'product_id': product_id,
    }
    print(order)
    # print(str(json.loads(json.dumps(order))))
    #r = requests.post(API_URL + 'orders', json=order, auth=auth)
    #return print(r.json())


def __get_best_bid_ask__(product_id):
    order_book_result = requests.get(API_URL + 'products/' + product_id + '/book?level=1', auth=auth)
    json_order_book = order_book_result.json()
    best_ask = json_order_book['asks'][0][0]
    best_bid = json_order_book['bids'][0][0]
    return {"ask": best_ask, "bid": best_bid}