def detect_sell_sar_updated(psar_latest, price_latest):
    if (psar_latest - price_latest) > 5:
        return True
    else:
        return False