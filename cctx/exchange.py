import ccxt

# Initialize exchange
print (ccxt.exchanges)
exchange = ccxt.kraken()

#TODO Authenticate for private APIs

# Fetch tickers from exchange
if (exchange.has['fetchTicker']):
    print(exchange.fetch_ticker('BTC/USD')) # ticker for LTC/ZEC
    symbols = list(exchange.markets.keys())