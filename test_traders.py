import unittest

from trader import Trader
from order import SideOrder


class TradersTest(unittest.TestCase):
    def test_create_orders(self):

        # Initial traders
        traders = []
        ntraders = 10
        for _ in range(ntraders):
            traders.append(Trader())

        # Initial Orders
        t1 = traders[0]
        t2 = traders[1]

        ticker = "GOOGLE"

        # Initial Buy orders
        b1 = t1.create_order(ticker, SideOrder.BUY, 10, 100)
        b2 = t1.create_order(ticker, SideOrder.BUY, 9, 200)
        b3 = t1.create_order(ticker, SideOrder.BUY, 9, 500)


        self.assertEqual(b1.ticker, ticker)
        self.assertEqual(b1.side, SideOrder.BUY)
        self.assertEqual(t1.account.money_hold, 10*100 + 9*200 + 9*500)

        # Initial Sell orders
        #s1 = t2.create_order(ticker, SideOrder.SELL, 12, 300)
        #s2 = t2.create_order(ticker, SideOrder.SELL, 13, 500)

        #self.assertEqual(s1.ticker, ticker)
        #self.assertEqual(s1.side, SideOrder.SELL)
        #self.assertEqual(b1.trader_id, t1.id)
        #self.assertEqual(b2.trader_id, t1.id)
        #self.assertEqual(b3.trader_id, t1.id)
        #s#elf.assertEqual(len(t1.created_orders),3)



        #self.assertEqual(s1.trader_id, t2.id)
        #self.assertEqual(s2.trader_id, t2.id)
        #self.assertEqual(len(t2.created_orders),2)
        #self.assertEqual(t1.account.money_hold, 12*300 + 9*200 + 9*500)


if __name__ == '__main__':
    unittest.main()
