import threading

import schedule
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.utils import iswrapper
from ibapi.wrapper import EWrapper

from GooseIndicatorMay import GooseIndicator, Signal

LAST_ORDER_ACTION=""
INITIAL_BUY_DONE=False

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.started = False
        self.globalCancelOnly = False

    @iswrapper
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

        self.start()

    def start(self):
        # print("inside start")

        if self.started:
            return

        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            # print("Executing requests")
            self.evaluateAndExecute()
            # print("Executing requests ... finished")

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)


    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def evaluateAndExecute(self):
        # print("Inside evaluateAndExecute")
        global LAST_ORDER_ACTION, INITIAL_BUY_DONE
        # Check if the signal is Buy or Sell
        actionType = GooseIndicator().deriveIndicatorAndPlaceOrder()
        order = Order()

        if actionType!= Signal.DO_NOTHING:

            if actionType.value == LAST_ORDER_ACTION:
                print('No Short or Long please. Moving on!')
            else:
                print("Last Action :: ",LAST_ORDER_ACTION, "  ,Current Action:: ",actionType.value)

                # Create order object
                order.totalQuantity = 1
                order.orderId = self.nextorderId
                order.orderType = 'MKT'
                order.isOmsContainer = False
                self.nextorderId += 1
                order.transmit = True

                if(INITIAL_BUY_DONE):
                    order.totalQuantity = 2
                    print ("initial buy done, order size is 2")

                if actionType == Signal.BUY:
                    order.action = 'BUY'
                elif actionType == Signal.SELL:
                    order.action = 'SELL'

                # place order
                self.placeOrder(self.nextorderId, SimpleFuture(), order)
                LAST_ORDER_ACTION = actionType.value
                INITIAL_BUY_DONE=True

        self.disconnect()
        # print ("exiting evalAndExecute")
       # time.sleep(3)

def SimpleFuture():
    #! [futcontract]
    contract = Contract()
    contract.symbol = "ES"
    contract.secType = "FUT"
    contract.exchange = "GLOBEX"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "202006"
    #! [futcontract]
    return contract

def job():
    app = IBapi()
    app.connect('127.0.0.1', 7497, 123)
    app.run()
    #app.evaluateAndExecute()
    #app.disconnect()
    # print("called goose")

schedule.every(1).second.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
