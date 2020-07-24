import ccxt
import time
import numpy as np
import tulipy as ti
import atexit
import sys
from pynput import keyboard

from ccxt import RequestTimeout

import test_util.test_util as test_util
import psar_ops.detect_buy_sar as detect_buy_sar
import psar_ops.detect_sell_sar as detect_sell_sar
# from test_util.test_metrics import TestMetrics
from util.visualization import display_metrics

exchange = ccxt.kraken({
    'enableRateLimit': True,
    'options': {  # ←--------------------- inside 'options' subkey
        'fetchMinOrderAmounts': False,  # ←---------- set to False
    }
})

# Set up test metrics instance
test_metrics_instance = TestMetrics()

# Set up general params
holding = False;
last_buy_price = 0
num_buys = 0
num_sells = 0
profit = 0
fees = 0;

# Set up live params
polling_interval_seconds = 1
history_length = 86400 # 86400 seconds in a day
acc_step = np.array(.02)
acc_max = np.array(.2)
symbol = 'BTC/USD'

#TODO Just fetch the last history_length and copy to history, don't worry about time steps at first...
# Fetch open high low close volume history
if (exchange.has['fetchOHLCV']):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d')
    print('OHLCV data fetched');

if (exchange.has['fetchTicker']):
    # Init vanilla arrays to read in ohlcv data
    ticker_low_history_vanilla = []
    ticker_bid_history_vanilla = []
    ticker_high_history_vanilla = []

    # Construct np array from vanilla
    ticker_low_history = np.array(ticker_low_history_vanilla)
    ticker_bid_history = np.array(ticker_bid_history_vanilla)
    ticker_high_history = np.array(ticker_high_history_vanilla)

    # Handle Ensenada exit
    def print_stats():
        print("Ensenada is exiting...")
        print("Num buys: " + str(num_buys))
        print("Num sells: " + str(num_sells))
        print("Gross profit: " + str(profit))
        print("Fees: " + str(fees))
        print("Net profit: " + str(profit - fees))

        test_metrics_instance.num_buys = num_buys;
        test_metrics_instance.num_sells = num_sells;
        test_metrics_instance.fees = fees;
        test_metrics_instance.profit = profit;

        display_metrics(test_metrics_instance, ticker_bid_history, psar)


    def on_press(key):
        try:
            if key.char == 'p':
                print_stats()
        except AttributeError:
            print('special key {0} pressed'.format(
                key))


    # ...or, in a non-blocking fashion:p
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    # Register exit function
    #TODO matplotlib will not be able to display for an exited process
    @atexit.register
    def at_exit():
        print_stats()
        print("Ensenada has exited.")

    # Every x time interval
    while True:
        # Add current ticker info to history

        try:
            ticker = exchange.fetch_ticker(symbol)
            current_low = ticker['low']
            current_bid = ticker['bid']
            current_high = ticker['high']
        except ConnectionResetError as connection_reset_error:
            print("ConnectionResetError: " + str(connection_reset_error))
            time.sleep(polling_interval_seconds)
            continue
            # raise
        except RequestTimeout as request_timeout_error:
            print("ConnectionResetError: " + str(request_timeout_error))
            time.sleep(polling_interval_seconds)
            continue
            # raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            time.sleep(polling_interval_seconds)
            continue
            # raise

        # Live data print
        print('Current bid: ' + str(current_bid))

        # Add current values to value history
        ticker_low_history = test_util.add_to_ticker_history_np(ticker_low_history, current_low, history_length)
        ticker_bid_history = test_util.add_to_ticker_history_np(ticker_bid_history, current_bid, history_length)
        ticker_high_history = test_util.add_to_ticker_history_np(ticker_high_history, current_high, history_length)

        # Ensure that we have passed the minimum for psar measurements
        if (len(ticker_bid_history) <= 10):#TODO 10 is arbitrary
            continue

        # Calculate PSAR for history
        psar = ti.psar(
            high=ticker_high_history,
            low=ticker_low_history,
            acceleration_factor_step=acc_step,
            acceleration_factor_maximum=acc_max
        )

        if(holding == False):
            # Detect PSAR for most recent x values
            execute_buy = detect_buy_sar.detect_buy_sar(psar[len(psar) - 1], current_bid)
            if (execute_buy):
                holding = True
                print('Executing buy at: ' + str(current_bid))
                last_buy_price = current_bid

                # Account for trading fees
                fees += current_bid * .00075
                num_buys += 1
        else:
            execute_sell = detect_sell_sar.detect_sell_sar(psar[len(psar) - 1], current_bid)
            if (execute_sell):
                holding = False
                print('Executing sell at: ' + str(current_bid))
                profit += current_bid - last_buy_price

                # Account for trading fees
                fees += current_bid * .00075
                num_sells += 1

        # Sleep a second before fetching new ticker info
        time.sleep(polling_interval_seconds)

else:
    print('No ticker info for at ' + exchange.hostname)