import MetaTrader5 as mt5
import pandas as pd
import ta


def get_symbol_info(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise Exception(f"Symbol {symbol} not found")

    return symbol_info


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


def sum_profit(positions):
    profit = 0

    for position in positions:
        profit += position.profit

    return profit
