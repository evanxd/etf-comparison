import json
import pandas as pd
import yfinance as yf

TICKERS = json.load(open("tickers.json", encoding="utf-8"))


def download(tickers, start, end):
    return [yf.download(ticker, start=start, end=end) for ticker in tickers]


def merge(data):
    names = ["Close_{i}".format(i=i) for i in range(len(data))]
    # Workaround: The name of the first Close column is not with "_0" suffix
    # when the length of ticker list is odd.
    names[0] = "Close" if len(data) % 2 != 0 else names[0]
    result = __merge(data)[names]

    new_names = {}
    for i, market in enumerate(TICKERS):
        new_names[names[i]] = market
    result.rename(new_names, axis=1, inplace=True)
    return result


def normalize(data):
    for d in data:
        d.Close = d.Close / max(d.Close)


def __merge(data, i=0):
    suffixes = (
        "_{left_suffix}".format(left_suffix=i),
        "_{right_suffix}".format(right_suffix=i+1)
    )
    if len(data) - 2 == i:
        return pd.merge(data[i], data[i+1], on="Date", suffixes=suffixes)
    else:
        return pd.merge(
            data[i], __merge(data, i=(i + 1)), on="Date", suffixes=suffixes
        )
