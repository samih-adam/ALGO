import json
import time as time_true
import pprint
import pathlib
import pandas as pd

from datetime import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from typing import List
from typing import Dict
from typing import Union
from typing import Optional

from pyrobot.trades import Trade
from pyrobot.portfolio import Portfolio
from pyrobot.stock_frame import StockFrame

from td.client import TDClient
from td.utils import milliseconds_since_epoch


class PyRobot():

    def __init__(self, client_id: str, redirect_uri: str, paper_trading: bool = True, credentials_path: Optional[str] = None, trading_account: Optional[str] = None) -> None:
        """Initalizes a new instance of the robot and logs into the API platform specified.











