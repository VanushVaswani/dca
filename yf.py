import yfinance as yf
data = yf.download('SPY.AX', start="2017-01-01")
data.to_csv('yfasx.csv')
