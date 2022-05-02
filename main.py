from trader import Trader
from market import Market

import logging
logger = logging.getLogger(__name__)

def process_create_order_or_cancel(reply_from_market_on_create_order: bool,
                               market : Market,
                               trader: Trader):
    if reply_from_market_on_create_order is not None:
        res = market.send_limit_order(reply_from_market_on_create_order)
        if res: # limit order send ok
            order_open_ok = trader.add_open_order(reply_from_market_on_create_order)
            if not order_open_ok:
                logger.warning("Open order was failed")
                return False
            logger.info("Order created in the market Ok")
            return True
        else: # order rejected so cancel
            order_cancel_ok = trader.cancel_order(reply_from_market_on_create_order)
            if not order_cancel_ok:
                logger.warning("Order cancel failed")
            else:
                logger.info("Order cancel OK")
                return True

    else:
        logger.warning("Order creation was rejected by the market")
        return False

def find_trader_for_order(order, traders):
    logger.info("Finding trader for order id "+str(order.id))
    for trader in traders:
        if trader.id == order.trader_id:
            return trader
    return None

def send_limit_order_and_update_trader(order, market:Market, traders):
    logger.info("Sending limit order and update trader created")
    resp = market.send_limit_order(order)
    if resp:
        trader = find_trader_for_order(order, traders)
        if trader is not None:
            trader.add_open_order(order)
            return True
    return False


from order import SideOrder



def test_scenario():
    # Initial traders
    traders = []
    ntraders = 10
    for _ in range(ntraders):
        traders.append(Trader())

    # Initial Orders
    t1 = traders[0]
    t2 = traders[1]
    t3 = traders[2]


    # Initial Buy orders
    b1 = t1.create_order("GOOGLE", SideOrder.BUY, 10, 100)
    b2 = t1.create_order("GOOGLE", SideOrder.BUY, 9, 200)
    b3 = t1.create_order("GOOGLE", SideOrder.BUY, 9, 500)

    # Initial Sell orders
    s1 = t2.create_order("GOOGLE", SideOrder.BUY, 12, 300)
    s2 = t2.create_order("GOOGLE", SideOrder.BUY, 13, 500)
    s3 = t3.create_order("GOOGLE", SideOrder.BUY, 15, 1000)

    # Create Market
    market = Market("GOOGLE")
    init_orders = [s1,s2,s3,b1,b2,b3]
    for o in init_orders:
        logger.info(o)

    logger.info("Start Inserting Orders into Market")
    for idx, order in enumerate(init_orders):
        logger.info("init order "+str(order))
        res = send_limit_order_and_update_trader(order, market, traders)
        if res is False:
            logger.warning("Market order rejected or trader not found on order"+str(order.side))


    logger.info("Inserting new order")
    s4 = t2.create_order("GOOGLE",SideOrder.BUY,5,100)


    process_create_order_or_cancel(s4, market, t2)
    logger.info(market)
    for t in traders:
        logger.info(t)


def similation():
    pass

def main():
    logger.info("Start Main")
    #test_scenario()


if __name__ == "__main__":

    # set up logging to file
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt= datefmt,
                        filename='matching_engine.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    c_format = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s',
                                 datefmt=datefmt)
    console.setLevel(logging.INFO)
    console.setFormatter(c_format)
    logger.addHandler(console)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger.info("start main")
    main()


