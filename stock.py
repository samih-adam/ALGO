from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import av

# input your key here
key = 'XXX'

ts = TimeSeries(key)

aapl, meta = ts.get_daily(symbol="AAPL")
print(aapl["2020-07-29"])

class TechIndicators(av):
    def __init__(self, *args, **kwargs):
        super(TechIndicators, self).__init__(*args, **kwargs)
        self._append_type = False
        if self.output_format.lower() == 'csv':
            raise ValueError("Output Format {} is not compatible with the TechIndicators class".format(
                self.output_format.lower()))

    def get_sma(self):





















