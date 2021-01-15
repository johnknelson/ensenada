import time
from alpaca.trade import Trade

trade_period = 60;
trade = Trade()

# TODO While market is open
while True:
    print("Evaluating trade execution at: " + time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)'))
    trade.evaluate_and_execute_trade()
    time.sleep(trade_period)

# TODO After market closes, liquidate positions and exit script
