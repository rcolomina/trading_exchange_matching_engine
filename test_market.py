import unittest

from order import Order, SideOrder
from market import Market


class MarketTest(unittest.TestCase):

    def setUp(self) -> None:
        print("\n")
        self.orders = []

        self.ticker = "test"
        ticker = self.ticker

        # Simulate Buy Ordersorder
        trader_id = "jessy"
        side = SideOrder.BUY
        list_init_orders = [(123,1000),(121,5000),(123,100),(124,150),(122.5,1234)]
        for p in list_init_orders:
            self.orders.append(Order(trader_id, ticker, side, price=p[0], volume=p[1]))

        o3 = Order(trader_id, ticker, SideOrder.BUY, price=100, volume=4000)
        o4 = Order(trader_id, ticker, SideOrder.BUY, price=120, volume=5000)


    # Simulate order
        trader_id = "larry"
        side = SideOrder.SELL

        o1 = Order(trader_id, ticker, side, price=150, volume=10000)
        self.orders.append(o1)
        o2 = Order(trader_id, ticker, side, price=158, volume=20000)
        self.orders.append(o2)
        self.orders.append(Order(trader_id, ticker, side, price=155, volume=100))
        self.orders.append(Order(trader_id, ticker, side, price=160, volume=200))
        self.orders.append(Order(trader_id, ticker, side, price=149, volume=250))
        self.orders.append(Order(trader_id, ticker, side, price=149, volume=250))
        self.orders.append(Order(trader_id, ticker, side, price=149.01, volume=250))


        self.market = Market(ticker)

        self.orders_small = [o1,o2,o3,o4]

    def test_send_limit_order_simple(self):
        for o in self.orders_small:
            ret = self.market.send_limit_order(o)
            #self.assertTrue(ret)
            print(self.market)

        trader_id = "asdf"
        market_order = Order(trader_id, self.ticker,SideOrder.BUY, None, volume=1000)
        self.market.send_market_order(market_order)
        print(self.market)

    def test_send_limit_order(self):
        # self.assertEqual(True, False)  # add assertion here
        # create market with ticker

        for o in self.orders:
            ret = self.market.send_limit_order(o)
            self.assertTrue(ret)
            print(self.market)
        #print([(o.price,o.volume) for o in self.market.sellers])
        #print([(o.price,o.volume) for o in self.market.buyers])

    def test_send_market_order(self):

        for o in self.orders:
            ret = self.market.send_limit_order(o)
            self.assertTrue(ret)
        print(self.market)

        trader_id = "attacker"
        my_market_order = Order(trader_id, self.ticker, SideOrder.BUY, None, 3000)

        realized_trades = self.market.send_market_order(my_market_order)

        for realized_order in realized_trades:
            print(realized_order)

        print(self.market)


    def test_send_market_order_sell(self):

        for o in self.orders:
            ret = self.market.send_limit_order(o)
            self.assertTrue(ret)
        print(self.market)

        trader_id = "attacker"
        my_market_order = Order(trader_id, self.ticker, SideOrder.SELL, None, 200)

        realized_trades = self.market.send_market_order(my_market_order)

        for realized_order in realized_trades:
            print(realized_order)

        print(self.market)


if __name__ == '__main__':
    unittest.main()
