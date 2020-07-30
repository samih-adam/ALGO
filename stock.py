from alpha_vantage.timeseries import TimeSeries


# input your key here
key = '7QZ7M7T8FHWLUAX1'

ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol="AAPL")
print(aapl["2020-07-29"])




