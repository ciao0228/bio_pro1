import pandas as pd
import numpy as np
import quandl  # 获取股票数据

from datetime import date
import matplotlib.pyplot as plt


# import pandas_datareader as web
# export QUANDL_API_KEY = "xxxxxxxx"   (这是临时的)
# web.DataReader('AAPL','quandl',datetime.datetime(2001,1,1),datetime.datetime(2002,1,1))

# config InlineBackend.figure_format = 'retina'

# 创建空的DataFrame变量，用于存储股票数据
StockPrices = pd.DataFrame()

# 设置股票数据的开始和结束的时间
start = date(2016, 12, 30)
end = date(2016, 12, 31)

# 创建股票代码的列表
ticker_list = ['AAPL', 'MSFT', 'XOM', 'JNJ', 'JPM', 'AMZN', 'GE', 'FB', 'T']

# 使用循环，挨个获取每只股票的数据，并存储调整后的收盘价
for ticker in ticker_list:
    data = quandl.get('WIKI/' + ticker, start_date=start, end_date=end)
    StockPrices[ticker] = data['Adj. Close']  # 注意 Adj. 和 Close 之间有一空格

# 输出数据的前5行
print(StockPrices.head())

StockReturns = StockPrices.pct_change().dropna()
# 打印前5行数据
print(StockReturns.head())

# StockReturns = pd.read_csv('StockReturns2017.csv', parse_dates=['Date'], index_col='Date')

portfolio_weights = np.array([0.12, 0.15, 0.08, 0.05, 0.09, 0.10, 0.11, 0.14, 0.16])

# 将收益率数据拷贝到新的变量 stock_return 中，这是为了后续调用的方便
stock_return = StockReturns.copy()

# 计算加权的股票收益
WeightedReturns = stock_return.mul(portfolio_weights, axis=1)

# 计算投资组合的收益
StockReturns['Portfolio'] = WeightedReturns.sum(axis=1)

# 绘制组合收益随时间变化的图
StockReturns.Portfolio.plot()
plt.show()

CumulativeReturns = ((1 + StockReturns["Portfolio"]).cumprod() - 1)
CumulativeReturns.plot()
plt.show()
