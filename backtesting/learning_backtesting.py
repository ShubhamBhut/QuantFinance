import datetime as dt
import talib
import yfinance as yf
import pandas_datareader as web
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 50)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


class MyMACDStrategy(Strategy):
    def init(self):
        price = self.data.Close
        self.macd = self.I(lambda x: talib.MACD(x)[0], price)
        self.macd_signal = self.I(lambda x: talib.MACD(x)[1], price)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()


class MyRSIStrategy(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        price = self.data.Close
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        if crossover(self.lower_bound, self.rsi):
            self.buy()


start_date = dt.datetime(2018, 1, 1)
end_date = dt.datetime(2022, 1, 1)

interval = "1d"
data = yf.download("^NSEI", start_date, end_date, interval=interval)
# data = web.DataReader("AAPL", "stooq", start_date, end_date)
bt = Backtest(data, MyRSIStrategy, commission=0.02, exclusive_orders=True)
stats = bt.optimize(
    upper_bound=range(40, 85, 5),
    lower_bound=range(10, 55, 5),
    rsi_window=range(10, 30, 2),
    maximize="Return [%]",
    constraint=lambda params: params.upper_bound > params.lower_bound,
    max_tries=500,
)

print(stats)
bt.plot()
