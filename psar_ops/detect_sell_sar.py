def detect_sell_sar(psar_latest, price_latest):
    if(psar_latest > price_latest):
        return True
    else:
        return False