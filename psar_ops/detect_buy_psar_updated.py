def detect_buy_sar_updated(psar_latest, price_latest):
    if (psar_latest - price_latest) < -20:
        return True
    else:
        return False