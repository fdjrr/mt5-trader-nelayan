import json
import time

import MetaTrader5 as mt5
from loguru import logger

from src.mt5_client import (
    close_position,
    get_positions,
    get_rates,
    get_symbol_info,
    total_profit,
)


class TraderNelayan:
    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)

            symbol = config["v2"]["symbol"]
            timeframe = config["v2"]["timeframe"]
            order_type = config["v2"]["order_type"]
            lot_size = config["v2"]["lot_size"]
            point = config["v2"]["point"]
            layers = config["v2"]["layers"]
            max_profit = config["v2"]["max_profit"]
            max_loss = config["v2"]["max_loss"]
            deviation = config["v2"]["deviation"]
            magic = config["v2"]["magic"]
            rsi_length = config["v2"]["rsi_length"]
            rsi_overbought = config["v2"]["rsi_overbought"]
            rsi_oversold = config["v2"]["rsi_oversold"]
            sleep = config["v2"]["sleep"]

        if order_type != "BUY" and order_type != "SELL":
            logger.error("Invalid order type")
            quit()

        if timeframe == "M1":
            self.timeframe = mt5.TIMEFRAME_M1
        elif timeframe == "M5":
            self.timeframe = mt5.TIMEFRAME_M5
        elif timeframe == "M15":
            self.timeframe = mt5.TIMEFRAME_M15
        elif timeframe == "M30":
            self.timeframe = mt5.TIMEFRAME_M30
        elif timeframe == "H1":
            self.timeframe = mt5.TIMEFRAME_H1
        elif timeframe == "H4":
            self.timeframe = mt5.TIMEFRAME_H4
        else:
            logger.error("Invalid timeframe")
            quit()

        self.symbol = symbol
        self.lot_size = lot_size
        self.point = point
        self.layers = layers
        self.max_profit = max_profit
        self.max_loss = max_loss
        self.deviation = deviation
        self.magic = magic
        self.rsi_length = rsi_length
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold

        self.sleep = sleep

    def run(self):
        symbol_info = get_symbol_info(self.symbol)
        logger.info(symbol_info)

        while True:
            logger.info("Fetching rates...")
            rates = get_rates(self.symbol, self.timeframe, self.rsi_length)

            logger.info("Checking if already in position...")
            positions = get_positions(self.symbol)

            profit = total_profit(positions)
            logger.info(f"Total Profit: {profit}")

            if profit <= self.max_loss or profit >= self.max_profit:
                logger.info("Closing all positions...")

                for position in positions:
                    close_position(position)

            last_rsi = rates["rsi"].iloc[-1]
            logger.info(f"Last RSI: {last_rsi}")

            if last_rsi >= self.rsi_overbought:
                logger.info("Signal Detected! RSI is overbought...")

                if len(positions) == 0:
                    symbol_info = get_symbol_info(self.symbol)
                    bid = symbol_info.bid

                    logger.info("opening SELL position...")
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": self.symbol,
                        "type": mt5.ORDER_TYPE_SELL,
                        "price": bid,
                        "volume": self.lot_size,
                        "deviation": self.deviation,
                        "magic": self.magic,
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_IOC,
                    }
                    result = mt5.order_send(request)
                    logger.info(result)

                    logger.info("Opening SELL_STOP layers...")
                    last_price = bid

                    for x in range(self.layers):
                        request = {
                            "action": mt5.TRADE_ACTION_PENDING,
                            "symbol": self.symbol,
                            "type": mt5.ORDER_TYPE_SELL_STOP,
                            "price": last_price,
                            "volume": self.lot_size,
                            "deviation": self.deviation,
                            "magic": self.magic,
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_IOC,
                        }
                        result = mt5.order_send(request)
                        logger.info(result)

                        last_price -= self.point
                else:
                    logger.info("Already in position...")

            elif last_rsi <= self.rsi_oversold:
                logger.info("Signal Detected! RSI is oversold....")

                logger.info("Checking if already in position...")
                positions = get_positions(self.symbol)

                if len(positions) == 0:
                    symbol_info = get_symbol_info(self.symbol)
                    ask = symbol_info.ask

                    logger.info("opening BUY position...")

                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": self.symbol,
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": ask,
                        "volume": self.lot_size,
                        "deviation": self.deviation,
                        "magic": self.magic,
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_IOC,
                    }

                    result = mt5.order_send(request)
                    logger.info(result)

                    logger.info("Opening BUY_STOP position...")
                    last_price = ask

                    for x in range(self.layers):
                        request = {
                            "action": mt5.TRADE_ACTION_PENDING,
                            "symbol": self.symbol,
                            "type": mt5.ORDER_TYPE_BUY_STOP,
                            "price": last_price,
                            "volume": self.lot_size,
                            "deviation": self.deviation,
                            "magic": self.magic,
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_IOC,
                        }

                        result = mt5.order_send(request)
                        logger.info(result)

                        last_price += self.point
                else:
                    logger.info("Already in position...")

            else:
                logger.info("No signal detected...")

            time.sleep(self.sleep)


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
