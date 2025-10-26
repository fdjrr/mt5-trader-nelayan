import MetaTrader5 as mt5
import pandas as pd
import ta


def get_symbol_info(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise Exception(f"Symbol {symbol} not found")

    return symbol_info


def get_rates(symbol=None, timeframe=None, rsi_length=14, n=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    if rsi_length:
        df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=rsi_length).rsi()

    return df


def get_positions(symbol):
    positions = mt5.positions_get(symbol=symbol)

    return positions


def get_orders(symbol):
    orders = mt5.orders_get(symbol=symbol)

    return orders


def get_order_prices(symbol):
    orders = get_orders(symbol)

    prices = []

    if orders:
        prices = [order.price_open for order in orders]

    return prices


def get_copy_rates(symbol, tf, indicators=None, n=100):
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, n)

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    if indicators is not None:
        for indicator, params in indicators.items():
            if indicator == "RSI":
                df["rsi"] = ta.momentum.rsi(df["close"], window=params["length"])

    return df


def open_position():
    pass


def modify_position():
    pass


def close_position(position):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": position.symbol,
        "type": (
            mt5.ORDER_TYPE_SELL
            if position.type == mt5.ORDER_TYPE_BUY
            else mt5.ORDER_TYPE_BUY
        ),
        "position": position.ticket,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    result = mt5.order_send(request)

    return result


def total_profit(positions):
    profit = 0

    for position in positions:
        profit += position.profit

    return profit
