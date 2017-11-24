import cmd
import os
import json

import historic_plotter
import trading

from GdaxExchangeAuth import GdaxExchangeAuth

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_PASS = os.environ['API_PASS']
API_URL = os.environ['API_URL']
auth = GdaxExchangeAuth(API_KEY, API_SECRET, API_PASS)


class GdaxTrader(cmd.Cmd):
    """Simple command processor example."""

    prompt = '>: '
    intro = "GDAX Trader Utility"

    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'

    def do_update(self, line):
        args = line.split()
        if len(args) != 2:
            print("Usage: update eth <new price>")
        else:
            product_id = args[0]
            new_price = args[1]
            trading.update_order_price(product_id, new_price)

    def do_buy(self, line):
        if len(line) == 0:
            print("Usage: buy 1 ETH")
        else:
            args = line.split()
            if len(args) == 3:
                amount = args[0]
                product = args[1]
                price = args[2]
                trading.limit_order(amount, 'buy', product, price)
            elif len(args) == 2:
                amount = args[0]
                product = args[1]
                trading.limit_order(amount, 'buy', product)
            elif len(args) == 1:
                product = args[0]
                trading.limit_order(-1, 'buy', product)

    def do_sell(self, line):
        if len(line) == 0:
            print("Usage: sell 1 ETH")
        else:
            args = line.split()
            if len(args) == 2:
                amount = args[0]
                product = args[1]
                trading.limit_order(amount, 'sell', product)
            else:
                product = args[0]
                trading.limit_order(-1, 'sell', product)

    def do_cancel(self, line):
        trading.cancel_order()

    def do_plot(self, line):
        args = line.split()
        if len(args) == 2:
            product_id = args[0]
            interval = args[1]
            historic_plotter.plot(product_id, interval)
        elif len(args) == 1:
            product_id = args[0]
            historic_plotter.plot(product_id, 3600)

    def do_fiat(self, line):
        print(trading.get_account_available('USD'))

    def do_eth(self, line):
        print(trading.get_account_available('ETH'))

    def do_btc(self, line):
        print(trading.get_account_available('BTC'))

    def do_ltc(self, line):
        print(trading.get_account_available('LTC'))

    def do_EOF(self, line):
        return True

    def do_help(self, line):
        print("Commands:")
        print("fiat / Get fiat balance")
        print("eth|btc|ltc / Get crypto balance")
        print("plot crypto [interval] | plot eth 3600")
        print("buy [amount] eth|btc|ltc e.g  buy 1 eth | buy eth (max amount)")
        print("sell [amount] eth|btc|ltc e.g  sell 1 eth | sell eth (sell all)")

    def do_quit(self, line):
        return True

if __name__ == '__main__':
    GdaxTrader().cmdloop()
