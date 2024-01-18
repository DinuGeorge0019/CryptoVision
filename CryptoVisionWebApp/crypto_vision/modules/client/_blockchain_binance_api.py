
import requests
from binance.client import Client
import datetime
import pandas as pd
import json

def get_crypto_average_prices(symbols):
    prices = {}
    for symbol in symbols:
        response = requests.get(f'https://api.binance.com/api/v3/avgPrice?symbol={symbol}')
        data = response.json()
        prices[symbol] = data['price']
    return prices

def get_crypto_current_prices(symbols):
    prices = {}
    for symbol in symbols:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}')
        data = response.json()
        prices[symbol] = data['price']
    return prices

def get_btc_24hr_ticker(symbols):
    ticker_data = []
    for symbol in symbols:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}')
        data = response.json()
        ticker_data.append(data)
    return ticker_data

def get_crypto_hystorical_data(symbol, days_in_the_past):
    client = Client()
    untilThisDate = datetime.datetime.now()
    sinceThisDate = untilThisDate - datetime.timedelta(days = days_in_the_past)
    
    # Execute the query from binance - timestamps must be converted to strings !
    candle = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_30MINUTE, str(sinceThisDate), str(untilThisDate))

    # Create a dataframe to label all the columns returned by binance so we work with them later.
    df = pd.DataFrame(candle, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

    # Get rid of columns we do not need
    df = df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'], axis=1)

    return df


def get_top_tokens(top_n=10):
    url = 'https://api.binance.com/api/v3/ticker/24hr?type=FULL'

    response = requests.get(url)
    data = response.json()

    # Filter the data to keep only instances where the symbol ends with 'USD'
    data = [item for item in data if item['symbol'].endswith('USD')]

    # Sorting the data based on the trading volume (24h)
    sorted_data = sorted(data, key=lambda x: float(x['quoteVolume']), reverse=True)

    # Extracting information for the top tokens
    top_tokens = sorted_data[:top_n]

    return top_tokens
