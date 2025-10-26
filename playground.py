import MetaTrader5 as mt5

from src.mt5_client import get_positions


def main():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    symbol = "BTCUSDc"

    positions = get_positions(symbol)

    print(positions)


if __name__ == "__main__":
    main()
