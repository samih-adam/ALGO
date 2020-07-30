from alpha_vantage.timeseries import TimeSeries
# input your key here
key = 'XXX'

ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol="AAPL")












