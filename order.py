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
        msg = "Order{uuid: " \
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
