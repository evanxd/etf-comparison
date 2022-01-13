from datetime import date
import json
import random
import streamlit as st

import utils

TICKERS = json.load(open("tickers.json", encoding="utf-8"))
tickers = [TICKERS[t] for t in TICKERS]

st.write("""
# ETF Comparison
""")

today = date.today()
start_date = st.date_input("Start Date", today.replace(year=today.year - 10))
end_date = st.date_input("End Date", today)

data = utils.download(tickers, start=start_date, end=end_date)
utils.normalize(data)

names = ["Close_{i}".format(i=i) for i in range(len(data))]
# Workaround: The name of the first Close column is not with "_0" suffix
# when the length of ticker list is odd.
names[0] = "Close" if len(data) % 2 != 0 else names[0]
result = utils.merge(data)[names]

new_names = {}
for i, market in enumerate(TICKERS):
    new_names[names[i]] = market
result.rename(new_names, axis=1, inplace=True)

markets = [market for market in TICKERS]
container = st.container()
all = st.checkbox("Pick All")

if all:
    selected_markets = container.multiselect('Pick ETFs', markets, markets)
elif "default_selected_markets" not in st.session_state:
    default_selected_markets = [markets[0]]
    default_selected_markets.extend(random.sample(markets[1:], 2))
    st.session_state["default_selected_markets"] = default_selected_markets
    selected_markets = container.multiselect(
        'Pick ETFs', markets, default_selected_markets
    )
else:
    selected_markets = container.multiselect(
        'Pick ETFs', markets, st.session_state["default_selected_markets"]
    )

if len(selected_markets) > 0:
    st.line_chart(result[selected_markets])
