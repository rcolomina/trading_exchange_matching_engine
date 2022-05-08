import uuid

from enum import Enum, unique


@unique
class SideOrder(Enum):
    BUY = "buy"
    SELL = "sell"


class MarketOrder:
    pass


class Order:
    def __init__(self, trader_id, ticker, side, price, volume):
        self.id = uuid.uuid4()
        self.trader_id = trader_id
        self.ticker = ticker
        self.side = side
        self.price = price
        self.volume = volume

    def __repr__(self):
        msg = "Order{id: " \
              + str(self.id) \
              + ",trader id: " \
              + str(self.trader_id) \
              + ",self.ticker: " \
              + str(self.ticker) \
              + ",side: " \
              + str(self.side) \
              + ",price: " \
              + str(self.price) \
              + ",volume: " \
              + str(self.volume) \
              + "}"
        return msg


class RealizedOrder:
    def __init__(self, trader_origin, trader_destiny, ticker, order_type, price, volume):
        self.id = uuid.uuid4()
        self.trader_origin = trader_origin
        self.trader_destiny = trader_destiny
        self.ticker = ticker
        self.order_type = order_type
        self.price = price
        self.volume = volume

    def __repr__(self):
        msg = "RealizedOrder{id: " \
              + str(self.id) \
              + ",trader origin id: " \
              + str(self.trader_origin) \
              + ",trader destiny id: " \
              + str(self.trader_destiny) \
              + ",ticker: " \
              + str(self.ticker) \
              + ",order_ticker: " \
              + str(self.order_type) \
              + ",order_price: " \
              + str(self.price) \
              + ",volume: " \
              + str(self.volume) \
              + "}"
        return msg
