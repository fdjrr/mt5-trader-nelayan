import MetaTrader5 as mt5


class TraderNelayan:
    def __init__(self, symbol, lot_size, start_price, end_price, point, order_type):
        self.symbol = symbol
        self.lot_size = lot_size
        self.start_price = start_price
        self.end_price = end_price
        self.point = point
        self.order_type = order_type
        self.deviation = 20
        self.magic = 234000

        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()

        pass

    def get_symbol_info(self):
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info is None:
            raise Exception(f"Symbol {self.symbol} not found")
        return symbol_info

    def order_send(self, order_type, price):
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": order_type,
            "price": price,
            "deviation": self.deviation,
            "magic": self.magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)

        return result

    def set_jaring(self, symbol_info):
        ask = symbol_info.ask
        bid = symbol_info.bid

        last_price = self.start_price

        while True:
            if self.end_price > last_price:
                break

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

            result = self.order_send(order_type, last_price)
            print(result)

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("order_send() failed, retcode={}".format(result.retcode))
                break

            last_price -= self.point


def main():
    try:
        print("MetaTrader5 package author: ", mt5.__author__)
        print("MetaTrader5 package version: ", mt5.__version__)

        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        symbol = str(input("Symbol: "))
        lot_size = float(input("Lot Size: "))
        start_price = float(input("Start Price: "))
        end_price = float(input("End Price: "))
        point = int(input("Point: "))
        order_type = str(input("Order Type (BUY, SELL): ")).upper()

        if order_type == "BUY":
            pass
        elif order_type == "SELL":
            pass
        else:
            print("Invalid order type")
            quit()

        traderNelayan = TraderNelayan(
            symbol, lot_size, start_price, end_price, point, order_type
        )

        symbol_info = traderNelayan.get_symbol_info()
        print(symbol_info)

        traderNelayan.set_jaring(symbol_info)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
