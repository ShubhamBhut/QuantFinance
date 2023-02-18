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


start_date = dt.datetime(2022, 1, 1)
end_date = dt.datetime(2022, 6, 1)

interval = "15m"
data = yf.download("AAPL", start_date, end_date, interval=interval)
# data = web.DataReader("AAPL", "stooq", start_date, end_date)
backtest = Backtest(data, MyMACDStrategy, commission=0.02, exclusive_orders=True)
print(backtest.run())
backtest.plot()
