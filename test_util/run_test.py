import matplotlib.pyplot as plt

import generic_ops.detect_buy as detect_buy
import generic_ops.detect_sell as detect_sell
# from test_util import test_metrics


def run_test(slice_size, price_list):

    # Begin detecting buy/sell, examining plots of 30 seconds
    # Initialize variables
    holding = False;
    buys = []
    sells = []
    num_buys = 0
    num_sells = 0
    holding_indices = []
    last_buy_price = 0
    profit = 0
    fees = 0

    # Begin iteration
    for ind, val in enumerate(price_list):
        if(ind <= slice_size):
            continue

        # Record the times during which we are holding
        if(holding == True):
            holding_indices.append(ind)

        # If we aren't holding, detect whether or not to buy
        if(holding == False):
            execute_buy = detect_buy.detect_buy(price_list[ind - slice_size:ind - 1])
            if(execute_buy):
                # Account for Kraken trading fees (.26% for takers on Kraken)
                fees += price_list[ind] * .001
                num_buys += 1

                holding = True
                last_buy_price = price_list[ind]
                buys.append(ind)
        # Else if we are holding, detect when to sell
        else:
            execute_sell = detect_sell.detect_sell(price_list[ind - slice_size:ind - 1]);
            if (execute_sell):
                # Account for Kraken trading fees (.16% for makers on Kraken)
                fees += price_list[ind] * .001
                num_sells += 1

                holding = False
                profit += price_list[ind] - last_buy_price
                sells.append(ind)

    test_metrics_instance = test_metrics.TestMetrics()
    test_metrics_instance.buys = buys
    test_metrics_instance.sells = sells
    test_metrics_instance.num_buys = num_buys
    test_metrics_instance.num_sells = num_sells
    test_metrics_instance.holding_indices = holding_indices
    test_metrics_instance.profit = profit
    test_metrics_instance.fees = fees

    return test_metrics_instance