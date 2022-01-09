import pandas as pd
import yfinance as yf

def download(tickers, start, end):
    return [yf.download(ticker, start=start, end=end) for ticker in tickers]

def merge(data, i=0):
    suffixes = ("_{left_suffix}".format(left_suffix=i), "_{right_suffix}".format(right_suffix=i+1))
    if len(data) - 2 == i:
        return pd.merge(data[i], data[i+1], on="Date", suffixes=suffixes)
    else:
        return pd.merge(data[i], merge(data, i=(i + 1)), on="Date", suffixes=suffixes)

def normalize(data):
    for d in data:
        d.Close = d.Close / max(d.Close)
