import tulipy as ti
import numpy as np

import psar_ops.detect_buy_sar as detect_buy_sar
import psar_ops.detect_sell_sar as detect_sell_sar
# from test_util import test_metrics

def run_test_sequential(price_df, acc_step, acc_max):

    # Begin detecting buy/sell, examining plots of 30 seconds
    # Initialize variables
    holding = False
    buys = []
    sells = []
    holding_indices = []
    last_buy_price = 0
    profit = 0

    # Create the running lists for all needed metrics
    price_open = price_df['open'].tolist()
    price_close = price_df['close'].tolist()
    price_high = price_df['high'].tolist()
    price_low = price_df['low'].tolist()

    # Create running price list
    running_open_list = [];
    running_close_list = [];
    running_high_list = [];
    running_low_list = [];

    # Begin iteration
    for ind, val in enumerate(price_open):
        # Capture current price
        current_price = price_open[ind]
        running_open_list.append(current_price)
        running_close_list.append(price_close[ind])
        running_high_list.append(price_high[ind])
        running_low_list.append(price_low[ind])

        # Ensure that we have passed the minimum for psar measurements
        if(ind <= acc_step):
            continue

        # Prepare np arrays for current PSAR inputs
        price_high_np = np.array(price_high);
        price_low_np = np.array(price_low);

        # Crunch PSAR for the info we currently know
        psar = ti.psar(high=price_high_np, low=price_low_np, acceleration_factor_step=acc_step,
                       acceleration_factor_maximum=acc_max)

        # Record the times during which we are holding
        if(holding == True):
            holding_indices.append(ind)

        # If we aren't holding, detect whether or not to buy
        if(holding == False):
            execute_buy = detect_buy_sar.detect_buy_sar(psar[ind - 1], running_open_list[ind - 1])
            if(execute_buy):
                holding = True
                last_buy_price = running_open_list[ind]
                buys.append(ind)
        # Else if we are holding, detect when to sell
        else:
            execute_sell = detect_sell_sar.detect_sell_sar(psar[ind - 1], running_open_list[ind - 1])
            if (execute_sell):
                holding = False
                profit += running_open_list[ind] - last_buy_price
                sells.append(ind)

    test_metrics_instance = test_metrics.TestMetrics()
    test_metrics_instance.buys = buys
    test_metrics_instance.sells = sells
    test_metrics_instance.holding_indices = holding_indices
    test_metrics_instance.profit = profit

    return test_metrics_instance