from datetime import date
import streamlit as st

import utils

st.write("""
# ETF Comparison
""")

today = date.today()
start_date = st.date_input("Start Date", today.replace(year=today.year - 10))
end_date = st.date_input("End Date", today)

data = utils.download(["VT", "SPY", "0050.TW"], start=start_date, end=end_date)
utils.normalize(data)

result = utils.merge(data)[["Close", "Close_1", "Close_2"]]
result.rename({"Close": "VT", "Close_1": "SPY", "Close_2": "0050.TW"}, axis=1, inplace=True)

st.write("""
## VT v. SPY v. 0050.TW
""")
st.line_chart(result)
