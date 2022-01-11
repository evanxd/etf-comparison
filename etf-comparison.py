from datetime import date
import re
import streamlit as st

import utils

TICKERS = {"Global (VT)": "VT", "Japan (EWJ)": "EWJ", "Korea (EWY)": "EWY", "Taiwan (0050.TW)": "0050.TW", "United States (SPY)": "SPY"}
tickers = [TICKERS[t] for t in TICKERS]

st.write("""
# ETF Comparison
""")

today = date.today()
start_date = st.date_input("Start Date", today.replace(year=today.year - 10))
end_date = st.date_input("End Date", today)

data = utils.download(tickers, start=start_date, end=end_date)
utils.normalize(data)

names = ["Close", "Close_1", "Close_2", "Close_3", "Close_4"]
result = utils.merge(data)[names]

new_names = {}
for i, market in enumerate(TICKERS):
    new_names[names[i]] = market
result.rename(new_names, axis=1, inplace=True)

markets = [market for market in TICKERS]
selected_markets = st.multiselect('Pick ETFs', markets, markets)

if len(selected_markets) > 0:
    st.line_chart(result[selected_markets])
