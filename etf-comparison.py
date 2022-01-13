from datetime import date
import random
import streamlit as st

import utils

TICKERS = utils.TICKERS
tickers = [TICKERS[t] for t in TICKERS]

st.write("""
# ETF Comparison
""")

today = date.today()
start_date = st.date_input("Start Date", today.replace(year=today.year - 10))
end_date = st.date_input("End Date", today)

data = utils.download(tickers, start=start_date, end=end_date)
utils.normalize(data)

container = st.container()
all = st.checkbox("Pick All")

markets = [market for market in TICKERS]
if "default_selected_markets" not in st.session_state:
    default_selected_markets = [markets[0]]
    default_selected_markets.extend(random.sample(markets[1:], 2))
    st.session_state["default_selected_markets"] = default_selected_markets
    selected_markets = container.multiselect(
        'Pick ETFs', markets, default_selected_markets
    )
elif all:
    selected_markets = container.multiselect('Pick ETFs', markets, markets)
else:
    selected_markets = container.multiselect(
        'Pick ETFs', markets, st.session_state["default_selected_markets"]
    )

result = utils.merge(data)
if len(selected_markets) > 0:
    st.line_chart(result[selected_markets])
