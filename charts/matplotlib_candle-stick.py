# Link below is really useful - CHECK IT ONCE ATLEAST
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mplfinance.original_flavor import candlestick_ohlc
import yfinance as yf

start_date = datetime.datetime(2021, 1, 1)
end_date = datetime.datetime(2022, 1, 1)

data = yf.download("AAPL", start_date, end_date)

data = data[["Open", "High", "Low", "Close"]]
data.reset_index(inplace=True)
