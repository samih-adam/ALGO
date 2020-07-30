from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.timeseries import as av


# input your key here
key = 'XXX'

ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol="AAPL")
print(aapl["2020-07-29"])

class TimeSeries(av):
    """this class implements all the api calls to time series
    """
    def get_intraday(self, symbol, interval='15min', outputsize='compact', __function_key='XXX'):
        """Return intraday time series in two json objects as data and meta_data.
        It raises ValueError when problems arise

        Keyword Arguments:
            symbol:TSLA
            interval: 30min
            outputsize:full

            """
        __function_key = "TIME_SERIES_INTRADAY"
        return __function_key, "Time Series ({})".format(interval), 'Meta Data'





