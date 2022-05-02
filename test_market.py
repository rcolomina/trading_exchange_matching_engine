import unittest

from order import Order, SideOrder
from market import Market


class MarketTest(unittest.TestCase):
    def test_send_limit_order(self):
        #self.assertEqual(True, False)  # add assertion here


        trader_id = "asdf"
        ticker = "test"
        side = SideOrder.BUY
        price = 123
        volume = 10000

        order = Order(trader_id,ticker,side,price,volume)

        trader_id = "asdfasdf3e"
        ticker = "test"
        side = SideOrder.SELL
        price = 150
        volume = 5000

        order2 = Order(trader_id,ticker,side,price,volume)

        market = Market(ticker)

        ret = market.send_limit_order(order)
        assert ret==True
        print(market)

        ret = market.send_limit_order(order2)
        assert ret==True
        print(market)



if __name__ == '__main__':
    unittest.main()
