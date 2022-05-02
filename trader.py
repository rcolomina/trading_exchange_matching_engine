import uuid
import random

from order import Order, SideOrder
from account import Account

import logging
logger = logging.getLogger(__name__)


class SideJob:
    def __init__(self, income, period):
        self.income = income
        self.period = period


class Trader:
    def __init__(self, money=1000000, risk_aversion=10, side_job=None):
        self.id = uuid.uuid4()

        # wallet
        self.account = Account(money, 0)

        # the trader has external source of income
        self.risk_aversion = risk_aversion

        # side job
        self.side_job = side_job

        # operations
        self.created_orders = []
        self.open_orders = []

        # knowledge of the market
        self.first_buyer = None
        self.first_seller = None

    def getId(self):
        return self.id

    def observe(self, market):

        self.first_seller = market.sellers[0]  # TODO: replace by getter checking length
        self.first_buyer  = market.buyer[0]  # TODO: replace by getter checking length

    def take_action(self):
        self.observe()
        random.randind(0, 10)

    def create_order(self, ticker: str, side: SideOrder, price: float, volume: float) -> Order:
        logger.info("Creating order for ticker " + ticker)
        # print("Creating order for ticker",ticker,"side",side,"price",price,"volume",volume)
        if self.account.enough_money(price, volume):

            if side is SideOrder.BUY:
                # hold money to buy
                if not self.account.lock_money(price, volume):
                    logger.warning("Not enough money to create buy order")
                    return None

            if side is SideOrder.SELL:
                # hold assets for sell
                if not self.account.hold_assets(price, volume):
                    logger.warning("Not enough assets to create sell order")
                    return None

            # order can be created
            order = Order(self.id, ticker, side, price, volume)

            # create the order
            self.created_orders.append(order)
            # print("created order",order)
            return order
        return None

    def cancel_oder(self, order_id: Order) -> bool:
        for created_order in self.created_orders:
            if order_id == created_order.id:
                self.created_orders.remove(created_order)
                if created_order.side == SideOrder.BUY:
                    if self.account.release_nomey(created_order.price, created_order.volume):
                        logger.info("Buy order was canceled OK - money released")
                        return True
                if created_order.side == SideOrder.SELL:
                    if self.account.release_assets(created_order.ticker, created_order.volume):
                        logger.info("Sell order was canceled OK - assets released")
                        return True
        logger.warning("Order was not cancelled")
        return False

    def add_open_order(self, order: Order) -> bool:
        # move order from created order to open orders
        for created_order in self.created_orders:
            if order.id == created_order.id:
                self.open_orders.append(created_order)
                self.created_orders.remove(created_order)
                logger.info("Order opened in the market with success")
                return True
        logger.warning("A problem was found opening current order")
        return False

    def __repr__(self):
        rep = ["Trader{id: ", str(self.id), ",money: ", str(self.account.money), ",money_hold: ",
               "{0:10d} ".format(self.account.money_hold), ", # created orders: ",
               "".join(str(len(self.created_orders))), ", # open orders: ", "".join(str(len(self.open_orders))), "}"]
        return "".join(rep)
