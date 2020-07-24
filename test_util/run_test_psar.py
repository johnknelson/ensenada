import tulipy as ti

from test_util.test_metrics import TestMetrics


def run_test(price_list, price_high_np, price_low_np, acc_step, acc_max, detect_buy_sar, detect_sell_sar):

    # Begin detecting buy/sell, examining plots of 30 seconds
    # Initialize variables
    holding = False;
    buys = []
    sells = []
    holding_indices = []
    last_buy_price = 0
    num_buys = 0
    num_sells = 0
    profit = 0
    fees = 0;

    # Crunch PSAR
    psar = ti.psar(high=price_high_np, low=price_low_np, acceleration_factor_step=acc_step, acceleration_factor_maximum=acc_max)

    # Begin iteration
    for ind, val in enumerate(price_list):
        # Ensure that we have passed the minimum for psar measurements
        if(ind <= acc_step):
            continue

        # Record the times during which we are holding
        if(holding == True):
            holding_indices.append(ind)

        # If we aren't holding, detect whether or not to buy
        if(holding == False):
            execute_buy = detect_buy_sar(psar[ind-1], price_list[ind-1])
            if(execute_buy):
                holding = True
                last_buy_price = price_list[ind]

                # # Account for trading fees ($2.99 ex on coinbase for traces > $100)
                # profit -= 3;

                # Account for Kraken trading fees (.26% for takers on Kraken)
                fees += price_list[ind] * .00075
                num_buys +=1

                buys.append(ind)
        # Else if we are holding, detect when to sell
        else:
            execute_sell = detect_sell_sar(psar[ind-1], price_list[ind-1])
            if (execute_sell):
                holding = False
                profit += price_list[ind] - last_buy_price

                # # Account for trading fees ($2.99 ex on coinbase for traces > $100)
                # profit -= 3;

                # Account for Kraken trading fees (.16% for makers on Kraken)
                fees += price_list[ind] * .00075
                num_sells += 1

                sells.append(ind)

    test_metrics_instance = TestMetrics()
    test_metrics_instance.buys = buys
    test_metrics_instance.sells = sells
    test_metrics_instance.holding_indices = holding_indices
    test_metrics_instance.num_buys = num_buys
    test_metrics_instance.num_sells = num_sells
    test_metrics_instance.profit = profit
    test_metrics_instance.fees = fees
    test_metrics_instance.holding_profit = price_list[len(price_list) - 1] - price_list[0]

    return test_metrics_instance