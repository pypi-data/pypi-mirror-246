import os, sys
from dotenv import load_dotenv

load_dotenv()

DIR_NAME = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(DIR_NAME))
sys.path.append(root)

import ttxt


def getTtxtExchange(exchangeName):
    if exchangeName == "gateFutures":
        print("returned gateFuture")
        return ttxt.gateFutures(key=os.getenv("KEY"), secret=os.getenv("SECRET"))
    if exchangeName == "bybitFutures":
        print("returned bybitFutures")
        return ttxt.bybitFutures(key=os.getenv("KEY"), secret=os.getenv("SECRET"))
    else:
        print(f"Exchange not supported: {exchangeName}")

def test(exchangeName="", params={}):
    ttxtExchange = getTtxtExchange(exchangeName)
    # ttxtExchange = ttxt.gateFutures(key=os.getenv("KEY"), secret=os.getenv("SECRET"))

    if "ticker" in params and params["ticker"]:
        print("testing ticker...")
        try:
            resp = ttxtExchange.fetch_ticker(tickerToTest)
            print(resp)
        except Exception as e:
            print("ticker could not be fetched")
            print(e)
    if "balance" in params and params["balance"]:
        print("testing balance...")
        try:
            resp = ttxtExchange.fetch_balance()
            print(f"balance response: {resp}")
        except Exception as e:
            print("balance could not be fetched")
            print(e)
    if "createOrder" in params and params["createOrder"]:
        print("testing create order...")
        try:
            resp = ttxtExchange.create_order(symbol=tickerToTest, type="limit", amount=0.001, side="buy", price=43920.08)
            print(f"createOrder response: {resp}")
        except Exception as e:
            print("order could not be created")
            print(e)
    if "fetchOrder" in params and params["fetchOrder"]:
        print("testing fetch order...")
        try:
            resp = ttxtExchange.fetch_order(id="f3708d4e-24d6-4528-9037-764d03610479")
            print(f"fetchOrder response: {resp}")
        except Exception as e:
            print("order could not be fetched")
            print(e)
    if "cancelOrder" in params and params["cancelOrder"]:
        print("testing cancel order...")
        try:
            resp = ttxtExchange.cancel_order(id="f3708d4e-24d6-4528-9037-764d03610479", params={"symbol": tickerToTest})
            print(f"cancelOrder response: {resp}")
        except Exception as e:
            print("order could not be canceled")
            print(e)
    if "fetchOpenOrders" in params and params["fetchOpenOrders"]:
        print("testing open orders...")
        try:
            resp = ttxtExchange.fetch_open_orders(symbol=tickerToTest)
            print(f"fetchOpenOrders response: {resp}")
        except Exception as e:
            print("OpenOrders could not be fetched")
            print(e)


if __name__ == "__main__":
    tickerToTest = "BTC/USDT"
    testingParams = {"ticker": False, "balance": False, "createOrder": False, "fetchOrder": False, 
                     "cancelOrder": True, "fetchOpenOrders": False}
    test(params=testingParams, exchangeName="bybitFutures")