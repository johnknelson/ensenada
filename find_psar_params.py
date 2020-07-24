import os
import numpy

import test
import sys

best_profit = -sys.maxsize-1
best_profit_acc_step = 0
best_profit_max_acc_step = 0

# For all values of the PSAR params that we care about
for acc_step in numpy.arange(.01, .21, .02):
    for max_acc_step in numpy.arange(.2, 2.0, .2):
        for directory, subdirectories, file_names in os.walk('historical_data/BTC_json'):
            trading_profit_vs_holding_all_days = 0
            for file_name in file_names:
                file_name_full_path = os.path.abspath(os.path.join(directory, file_name))
                test_metrics_instance = test.test_for_dataset_psar(acc_step, max_acc_step, file_name_full_path, False)

                net_profits = test_metrics_instance.profit - test_metrics_instance.fees
                trading_profit_vs_holding = net_profits - test_metrics_instance.holding_profit
                trading_profit_vs_holding_all_days += trading_profit_vs_holding

        if trading_profit_vs_holding_all_days > best_profit:
            best_profit = trading_profit_vs_holding_all_days
            best_profit_acc_step = acc_step
            best_profit_max_acc_step = max_acc_step

print("best_profit: " + str(best_profit))
print("best_profit_acc_step: " + str(best_profit_acc_step))
print("best_profit__max_acc_step: " + str(best_profit_max_acc_step))