import time
from alpaca import evaluate_and_execute_trade

trade_period = 60;

while True:
    evaluate_and_execute_trade.evaluate_and_execute_trade()
    time.sleep(trade_period)


