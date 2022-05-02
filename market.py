import logging
logger = logging.getLogger(__name__)

from order import SideOrder




class Market:
    def __init__(self, ticker):
        self.ticker  = ticker
        self.buyers  = []
        self.sellers = []

        self.agg_buyers  = {}
        self.agg_sellers = {}

        self.historical_traders = []

    def _check_valid_order(self, order):
        ticker_ok = order.ticker is self.ticker
        order_ok  = order.side in [SideOrder.BUY, SideOrder.SELL]
        return ticker_ok and order_ok

    def _insert_order(self, order):
        len_buyers  = len(self.buyers)
        len_sellers = len(self.sellers)
        order_buy   = order.side == SideOrder.BUY
        void_book   = len_buyers == 0 and len_sellers == 0

        if void_book:
            side_order = self.buyers if order_buy else self.sellers
            side_order.append(order)
            return True

        if order_buy and len_sellers > 0:
            if order.price > self.sellers[0].price: # we cannot buy more expensive than the cheapest seller
                logger.warning("Problem inserting order")
                return False
            else:
                if len_buyers == 0:
                    self.buyers.append(order)
                    return True

        if not order_buy and len_buyers > 0:
            if order.price < self.buyers[0].price: # we cannot sell cheaper that the most expensive buyer
                logger.warning("Problem inserting order")
                return False
            else:
                if len_sellers == 0:
                    self.sellers.append(order)
                    return True

        length = len_buyers if order_buy else len_sellers
        index = 0
        while index < length:
            side_order = self.buyers if order_buy else self.sellers[::-1]
            if order.price > side_order[index].price:
                side_order.insert(index,order)
            index += 1
            #    if order.price > self.buyers[index].price:
            #        self.buyers.insert(index,order)
            #        return True
            #else:
            #    if order.price < self.sellers[index].price:
            #        self.sellers.insert(index,order)
            #        return True
            #index += 1
        logger.warning("Problem inserting order")
        return False

    def send_limit_order(self, order):

        is_ok = self._check_valid_order(order)
        if not is_ok:
            return False

        is_ok = self._insert_order(order)
        if not is_ok:
            return False

        return True

    def send_market_order(self, order):
        pass

    def cancel(self, order):
        if order.ticker is not self.ticker:
            logger.info("Warn: Incorrect Ticker")
            return False
        if order.side == SideOrder.BUY:
            pass
            #remove from list
        if order.side == SideOrder.SELL:
            pass


    def _update_orders(self, current_orders):
        map_prices_to_pairs_n_orders_volume = {}
        logger.info("Current Order "+str(current_orders))
        for o in current_orders:
            price = o.price
            vol = o.volume
            aggregate = map_prices_to_pairs_n_orders_volume.get(price)
            if aggregate is not None:
                updated_num_orders = aggregate[0] + 1
                updated_total_vol  = aggregate[1] + vol
                map_prices_to_pairs_n_orders_volume[price] = (updated_num_orders,
                                                             updated_total_vol)
            else:
                map_prices_to_pairs_n_orders_volume[price] = (1, vol)
        return map_prices_to_pairs_n_orders_volume

    def _update_aggregations(self):
        logger.info("Update aggregations for representation")
        self.agg_buyers  = self._update_orders(self.buyers)
        self.agg_sellers = self._update_orders(self.sellers)

    def __repr__(self):
        self._update_aggregations()

        def give_format_to_num(num):
            return "{0:05d}".format(num)

        rep = []
        market_name = f"{self.ticker} MARKET".ljust(99)
        rep.append(market_name+"\n")

        header = "# Buy Orders".ljust(14) \
                 + "Vol".ljust(5) \
                 + " " \
                 + "Ask".ljust(5) \
                 + " | " \
                 + "Bid".ljust(5) \
                 + " " \
                 + "Vol".ljust(5) \
                 + " " \
                 + "# Sell Orders ".ljust(12)
        rep.append(header + "\n")

        buy_prices  = list(self.agg_buyers.keys())
        sell_prices = list(self.agg_sellers.keys())
        for b, s in zip(buy_prices,sell_prices):
            b_price   = b
            b_order   = self.agg_buyers.get(b)[0]
            b_vol     = self.agg_buyers.get(b)[1]

            rep.append(str(b_order).rjust(12) + "  " + give_format_to_num(b_vol) + " " + give_format_to_num(b_price))
            rep.append(" | ")
            s_price   = s
            s_order   = self.agg_sellers.get(s)[0]
            s_vol     = self.agg_sellers.get(s)[1]

            rep.append(give_format_to_num(s_price) + " " + give_format_to_num(s_vol)+" " + str(s_order).ljust(12))

            rep.append("\n")
        return "".join(rep)