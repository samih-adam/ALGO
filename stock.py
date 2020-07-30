from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import json
from key import api_key
import pandas as pd

# input your key here
api_key = " "

ts = TimeSeries(api_key)

aapl, meta = ts.get_daily(symbol="AAPL")
print(aapl["2020-07-29"])

stock = input("What stock do you want to see")

def rsi_dataframe(stock=stock):
    api_key1 = api_key
    period = 60
    ts = TimeSeries(key=api_key,output_format='pandas')
    data_ts = ts.get_intraday(stock.upper(), interval='1min', outputsize='full')

    #indicator
    ti = TechIndicators(key=api_key, output_format='pandas')
    data_ti, meta_data_ti = ti.get_rsi(symbol=stock.upper(), interval='1min', time_period=period, series_type='close')
    
    df = data_ts
    return print(df)
rsi_dataframe()




