def detect_sell(prices):
    # Find difference between end and beginning of this snippet
    diff = prices[len(prices)-1] - prices[0]

    if(diff < 0):
        return True
    else:
        return False