import uuid

import logging

logger = logging.getLogger(__name__)

from enum import Enum, unique

@unique
class TicketAsset(Enum):
    GOOGLE  = "GOOGLE"
    BITCOIN = "BTC"

@unique
class TypeAsset(Enum):
    STOCK = "STOCK"
    CRYPT = "CRYPTO"
    COMMODITY = "COMMODITY"
    BOND = "BOND"

class Asset:
    def __init__(self, ticker: TicketAsset, type_asset: TypeAsset):
        self.ticker     = ticker
        self.type_asset = type_asset
    def __repr__(self):
        return "Asset{ticker:"+str(self.ticker)+",type_asset:"+str(self.type_asset)+"}"

class Account:
    def __init__(self, money, assets_volume, money_hold=0, assets_volume_hold={}):
        self.id = uuid.uuid4()

        self.money = money # actual money

        self.money_hold   = money_hold # money hold < money

        self.assets_volume = assets_volume

        self.assets_volume_hold  = {} # nothing is hold

        self.movements = [] # logg of movements

    def __repr__(self):
        return "Account{money:"+str(self.money)+",money_hold:"+str(self.money_hold)+"}"

    def enough_money(self, price, volume):
        return self.money >= price * volume

    def enough_assets(self, ticker, volume):
        asset_vol = self.assets_volume_hold.get(ticker)
        if asset_vol is not None:
            return asset_vol >= volume
        return False

    def lock_money(self, price, volume):
        if self.enough_money(price, volume):
            amount = price * volume
            self.money_hold += amount
            self.movements.append(("hold",amount))
            return True
        logger.warning("Not enough money to buy")

    def release_money(self, price, volume):
        amount = price * volume
        self.money_hold -= amount
        self.movements.append(("release",amount))

    def hold_assets(self, ticker, volume):
        #assets_in_account =
        if self.enough_assets(ticker, volume):
            self.assets_volume_hold[ticker] -= volume
            self.movements.append(("hold_asset",(ticker,volume)))
            return True
        logger.warning("Not enough assets to sell")
        return False

    def release_assets(self, ticker, volume):
        current_volume = self.asset_volume.get(ticker)
        if current_volume is not None:
            self.assets_volume_hold[ticker] = current_volume + volume
