from alpha_vantage.techindicators import av


class TechIndicators(av):
    def __init__(self, *args, **kwargs):
        super(TechIndicators, self).__init__(*args, **kwargs)
        self._append_type = False
        if self.output_format.lower() == 'csv':
            raise ValueError("Output Format {} is not compatible with the TechIndicators class".format(
                self.output_format.lower()))

    def get_sma(self, symbol, interval='daily', time_period=20, series_type='close'):
        """ return simple moving average time series in two json objects as data and meta_data. It raises ValueError
        when problems arise

        Keyword Arguments:
            symbol: AAPL
            interval: 15min
            time_period: 20
            series_type: high
            """
        __FUNCTION_KEY__ = "SMA"
        return __FUNCTION_KEY__, 'Technical Analysis: SMA', 'Meta Data'
