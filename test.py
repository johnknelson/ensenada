import json

import pandas as pd
import numpy as np
import tulipy as ti

import test_util.test_util as test_util
import test_util.run_test as run_test
import test_util.run_test_psar as run_test_psar
import test_util.run_test_sequential as run_test_sequential
from test_util.test_metrics import TestMetrics
from psar_ops import detect_sell_sar, detect_buy_sar, detect_sell_psar_updated, detect_buy_psar_updated
import util.tulip_util as tulip_util
from util.visualization import display_metrics


def test_for_dataset_psar(acc_step, acc_max, file_name, should_display_metric_visuals):
    # load data
    with open(file_name, 'r') as history_json_file:
        history = json.load(history_json_file)

    print('Loaded ' + str(len(history['Data'])) + ' minutes of currency data.');

    # Create the pandas DataFrames for price time-series fields
    price_df = pd.DataFrame(history['Data'])
    price_open = price_df['open'].tolist()
    price_close = price_df['close'].tolist()
    price_high = price_df['high'].tolist()
    price_low = price_df['low'].tolist()

    print('History data frame loaded');

    # Create numpy array
    price_list_np_array = np.array(price_open)

    # Expose info about tulip indicator for
    tulip_util.print_info(ti.rsi)
    tulip_util.print_info(ti.psar)

    # Try out tulip indicator on numpy array
    rsi = ti.rsi(price_list_np_array, 120)

    # high_low = np.array([price_high, price_low], np.int32)
    price_high_np = np.array(price_high);
    price_low_np = np.array(price_low);

    # Run PSAR
    psar = ti.psar(high=price_high_np, low=price_low_np, acceleration_factor_step=acc_step, acceleration_factor_maximum=acc_max)

    # Calculate total potential gains of time-series
    print("Total potential gains: " + str(test_util.calculate_potential_gains(price_df)))

    # Run desired test
    # test_metrics_instance = run_test.run_test(60, price_open)
    test_metrics_instance = run_test_psar.run_test(price_open,
                                                   price_high_np,
                                                   price_low_np,
                                                   acc_step,
                                                   acc_max,
                                                   detect_buy_sar.detect_buy_sar,
                                                   detect_sell_sar.detect_sell_sar)
                                                   # detect_buy_psar_updated.detect_buy_sar_updated,
                                                   # detect_sell_psar_updated.detect_sell_sar_updated)

    # test_metrics_instance = run_test_sequential.run_test_sequential(price_df, acc_step, acc_max)

    if should_display_metric_visuals:
        display_metrics(test_metrics_instance, price_open, psar, should_display_metric_visuals)

    return test_metrics_instance