import json

import MetaTrader5 as mt5
from loguru import logger

from src.mt5_client import get_order_prices, get_symbol_info


class TraderNelayan:
    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)

            symbol = config["v1"]["symbol"]
            order_type = config["v1"]["order_type"]
            lot_size = config["v1"]["lot_size"]
            point = config["v1"]["point"]
            start_price = config["v1"]["start_price"]
            end_price = config["v1"]["end_price"]
            deviation = config["v1"]["deviation"]
            magic = config["v1"]["magic"]

        if order_type != "BUY" and order_type != "SELL":
            logger.error("Invalid order type")
            quit()

        self.symbol = symbol
        self.order_type = order_type
        self.lot_size = lot_size
        self.point = point
        self.start_price = start_price
        self.end_price = end_price
        self.deviation = deviation
        self.magic = magic

    def run(self):
        symbol_info = get_symbol_info(self.symbol)
        logger.info(symbol_info)

        order_prices = get_order_prices(self.symbol)
        logger.info(order_prices)

        ask = symbol_info.ask
        bid = symbol_info.bid

        last_price = self.start_price

        while True:
            if self.end_price > last_price:
                break

            if last_price not in order_prices:
                if self.order_type == "BUY":
                    if last_price > ask:
                        order_type = mt5.ORDER_TYPE_BUY_STOP
                    else:
                        order_type = mt5.ORDER_TYPE_BUY_LIMIT
                else:
                    if last_price < bid:
                        order_type = mt5.ORDER_TYPE_SELL_STOP
                    else:
                        order_type = mt5.ORDER_TYPE_SELL_LIMIT

                request = {
                    "action": mt5.TRADE_ACTION_PENDING,
                    "symbol": self.symbol,
                    "volume": self.lot_size,
                    "type": order_type,
                    "price": last_price,
                    "deviation": self.deviation,
                    "magic": self.magic,
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_RETURN,
                }
                logger.info(request)

                result = mt5.order_send(request)
                logger.info(result)

                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    logger.error(
                        "order_send() failed, retcode={}".format(result.retcode)
                    )
                    break

            last_price -= self.point


def main():
    try:
        if not mt5.initialize():
            logger.error("initialize() failed, error code =", mt5.last_error())
            quit()

        logger.info(f"MetaTrader5 package author: {mt5.__author__}")
        logger.info(f"MetaTrader5 package version: {mt5.__version__}")

        traderNelayan = TraderNelayan()
        traderNelayan.run()

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
