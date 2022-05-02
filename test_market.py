import unittest

from order import Order, SideOrder
from market import Market


class MarketTest(unittest.TestCase):
    def test_send_limit_order(self):
        #self.assertEqual(True, False)  # add assertion here

        print("\n")

        # Simulate order
        trader_id = "asdf"
        ticker = "test"
        side = SideOrder.BUY
        price = 123
        volume = 1000

        order0 = Order(trader_id,ticker,side,price,volume)
        print(order0)

        price = 121
        volume = 5000
        order1 = Order(trader_id,ticker,side,price,volume)
        print(order1)

        # Simulate order
        trader_id = "asdfasdf3e"
        ticker = "test"
        side = SideOrder.SELL
        price = 150
        volume = 5000

        order2 = Order(trader_id,ticker,side,price,volume)
        print(order2)

        price = 151
        order3 = Order(trader_id,ticker,side,price,volume)
        print(order3)

        orders = [order1,order0,order2,order3]

        # create market with ticker
        market = Market(ticker)

        for o in orders:
            ret = market.send_limit_order(o)
            assert ret==True
            print(market)



if __name__ == '__main__':
    unittest.main()
