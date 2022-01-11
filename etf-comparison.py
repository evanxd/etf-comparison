from datetime import date
import re
import streamlit as st

import utils

TICKERS = { "Global": "VT", "US": "SPY", "TW": "0050.TW" }
tickers = [TICKERS[t] for t in TICKERS]

st.write("""
# ETF Comparison
""")

today = date.today()
start_date = st.date_input("Start Date", today.replace(year=today.year - 10))
end_date = st.date_input("End Date", today)

data = utils.download(tickers, start=start_date, end=end_date)
utils.normalize(data)

result = utils.merge(data)[["Close", "Close_1", "Close_2"]]
result.rename({"Close": tickers[0], "Close_1": tickers[1], "Close_2": tickers[2]}, axis=1, inplace=True)

selected_tickers = []
for market in TICKERS:
    checked = st.checkbox("{market} ({ticker})".format(market=market, ticker=TICKERS[market]), value=True)
    if checked:
        selected_tickers.append(TICKERS[market])

if len(selected_tickers) > 0:
    st.line_chart(result[selected_tickers])
