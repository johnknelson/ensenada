import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tulipy as ti

import test_util.test_util as test_util
import test_util.run_test as run_test
import test_util.run_test_psar as run_test_psar
import test_util.run_test_sequential as run_test_sequential
# from test_util.test_metrics import TestMetrics
import util.tulip_util as tulip_util

def display_metrics(test_metrics_instance, price_history, psar, should_display_metric_visuals):
    # Initialize plot
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.ylabel('Price History Vs. PSAR')
    plt.plot(price_history, 'r', label='price')
    plt.plot(psar, 'bo', markersize=1, label='PSAR')
    plt.legend()

    # Print statistics
    print("Trading profits: " + str(test_metrics_instance.profit))
    trading_return_percentage = test_metrics_instance.profit / price_history[0];
    print("Trading profit percentge: " + str(trading_return_percentage))
    print("Holding profits: " + str(test_metrics_instance.holding_profit))
    holding_return_percentage = test_metrics_instance.holding_profit / price_history[0];
    print("Holding profit percentge: " + str(holding_return_percentage))
    trading_fees = test_metrics_instance.fees;
    print("Trading fees: " + str(trading_fees))
    print("Num buys: " + str(test_metrics_instance.num_buys))
    print("Num sells: " + str(test_metrics_instance.num_sells))
    net_profits = test_metrics_instance.profit - test_metrics_instance.fees
    print("Net profits: " + str(net_profits))
    print("Trading net vs holding: " + str(net_profits - test_metrics_instance.holding_profit))

    # Plot holding indices
    plt.plot(test_metrics_instance.holding_indices,
             [price_history[len(price_history) - 1]] * len(test_metrics_instance.holding_indices), 'go',
             markersize=1)  # plot x and y using red circle markers

    # Show plot
    if should_display_metric_visuals:
        plt.show()
