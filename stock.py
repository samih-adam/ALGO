from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.timeseries import av
import pandas as pd

# input your key here
key = 'XXX'

ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol="AAPL")
print(aapl["2020-07-29"])


class TimeSeries(av):
    """this class implements all the api calls to time series
    """

    def get_intraday(self, symbol, interval='15min', outputsize='compact', key='XXX'):
        """Return intraday time series in two json objects as data and meta_data.
        It raises ValueError when problems arise

        Keyword Arguments:
            symbol:  the symbol for the equity we want to get its data
            interval:  time interval between two conscutive values,
                supported values are '1min', '5min', '15min', '30min', '60min'
                (default '15min')
            outputsize:  The size of the call, supported values are
                'compact' and 'full; the first returns the last 100 points in the
                data series, and 'full' returns the full-length intraday times
                series, commonly above 1MB (default 'compact')
            """
        symbol: TSLA
        interval: 15(min)
        outputsize: full


        key = "TIME_SERIES_INTRADAY"
        return key, "Time Series ({})".format(interval), 'Meta Data'
