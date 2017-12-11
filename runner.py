import gdax, time

order_book = gdax.OrderBook(product_id='ETH-USD')
order_book.start()

while True:
        time.sleep(15)
        print(order_book.get_nums())

order_book.close()