import json
import os
import sched
import time
import requests
import math

import trading


def buyin(product_id, re_base=False, stop_loss=0.1, take_profit=0.1, trailing_stop_loss=True):
    order_placed = trading.buy_best_limit(product_id)
    order_id = order_placed['id']
    order_bid = float(order_placed['price'])
    print("Order in at bid: " + str(order_bid))

    if re_base:
        order = trading.get_order(order_id)
        still_open = bool(order['settled']) is False
        while still_open:
            print("Order is still not settled")
            time.sleep(1)
            order = trading.get_order(order_id)
            still_open = bool(order['settled']) is False
            best_bid_now = float(trading.get_best_bid_ask(product_id)['bid'])-1.0
            time.sleep(1)
            print("Best bid now: " + str(best_bid_now))

            if best_bid_now > order_bid:
                print("Best bid has moved past our threshold")
                trading.cancel_order_by_id(order_id)
                order_placed = trading.buy_best_limit(product_id)
                if order_placed is None:
                    break
                order_id = order_placed['id']
                order_bid = float(order_placed['price'])

        # Should now have a filled order
        print("In position")
        best_ask_now = float(trading.get_best_bid_ask(product_id)['ask']) - 1.0
        print("Best ask now: " + str(best_ask_now))
        stop_loss_price = best_ask_now * (1.0 - stop_loss)
        print("Setting stop loss at " + str(stop_loss_price))
        take_profit_price = best_ask_now * (1.0 + take_profit)
        print("Setting take profit at " + str(take_profit_price))
        in_position = True
        while in_position:
            time.sleep(5)
            best_ask_now = float(trading.get_best_bid_ask(product_id)['ask']) - 1.0
            if best_ask_now >= take_profit_price or best_ask_now <= stop_loss_price:
                # sell
                size = order_placed['size']
                trading.limit_order(size, "sell", product_id)
                break





s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    s.enter(60, 1, do_something, (sc,))






# Get accounts
# r = requests.get(API_URL + 'orders?status=open', auth=auth)
#
# orders = r.json()
# for order in orders:
#     if order['status'] == 'open':
#         order_price = order['price']


if __name__ == "__main__":
    buyin("ETH-USD", True)
    #trail_pc = 5.0 / 100

    #limit_order(1, 'buy', 'ETH-USD')

    #s.enter(60, 1, do_something, (s,))
    #s.run()