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

       # """Initalizes a new instance of the robot and logs into the API platform specified
       Arguments:
       ----
       signals
       {list} - - A
       pandas.Series
       object
       representing
       the
       buy
       signals and sell
       signals.
       Will
       check if series is empty
       before
       making
       any
       trades.

    Trades:
    ----
    trades_to_execute
    {dict} - - the
    trades
    you
    want
    to
    execute if signals
    are
    found.
    Returns:
    ----
    {List[dict]} - - Returns
    all
    order
    responses.
    Usage:
    ----
    >> > trades_dict = {
        'MSFT': {
            'trade_func': trading_robot.trades['long_msft'],
            'trade_id': trading_robot.trades['long_msft'].trade_id
        }
    }
    >> > signals = indicator_client.check_signals()
    >> > trading_robot.execute_signals(
        signals=signals,
        trades_to_execute=trades_dict
    )


"""

buys: pd.Series = signals[0][1]
sells: pd.Series = signals[1][1]

order_responses = []

# If we have buys or sells continue.
if not buys.empty:

    # Grab the buy Symbols.
    symbols_list = buys.index.get_level_values(0).to_list()

    # Loop through each symbol.
    for symbol in symbols_list:

        # Check to see if there is a Trade object.
        if symbol in trades_to_execute:

            if self.portfolio.in_portfolio(symbol=symbol):
                self.portfolio.set_ownership_status(
                    symbol=symbol,
                    ownership=True
                )

            # Set the Execution Flag.
            trades_to_execute[symbol]['has_executed'] = True
            trade_obj: Trade = trades_to_execute[symbol]['trade_func']

            if not self.paper_trading:

                # Execute the order.
                order_response = self.execute_orders(
                    trade_obj=trade_obj
                )

                order_response = {
                    'order_id': order_response['order_id'],
                    'request_body': order_response['request_body'],
                    'timestamp': datetime.now().isoformat()
                }

                order_responses.append(order_response)

            else:

                order_response = {
                    'order_id': trade_obj._generate_order_id(),
                    'request_body': trade_obj.order,
                    'timestamp': datetime.now().isoformat()
                }

                order_responses.append(order_response)

elif not sells.empty:

    # Grab the buy Symbols.
    symbols_list = sells.index.get_level_values(0).to_list()

    # Loop through each symbol.
    for symbol in symbols_list:

        # Check to see if there is a Trade object.
        if symbol in trades_to_execute:

            # Set the Execution Flag.
            trades_to_execute[symbol]['has_executed'] = True

            if self.portfolio.in_portfolio(symbol=symbol):
                self.portfolio.set_ownership_status(
                    symbol=symbol,
                    ownership=False
                )

            trade_obj: Trade = trades_to_execute[symbol]['trade_func']

            if not self.paper_trading:

                # Execute the order.
                order_response = self.execute_orders(
                    trade_obj=trade_obj
                )

                order_response = {
                    'order_id': order_response['order_id'],
                    'request_body': order_response['request_body'],
                    'timestamp': datetime.now().isoformat()
                }

                order_responses.append(order_response)

            else:

                order_response = {
                    'order_id': trade_obj._generate_order_id(),
                    'request_body': trade_obj.order,
                    'timestamp': datetime.now().isoformat()
                }

                order_responses.append(order_response)

# Save the response.
self.save_orders(order_response_dict=order_responses)

return order_responses

def execute_orders(self, trade_obj: Trade) -> dict:
"""
Executes
a
Trade
Object.
Overview:
----
The
`execute_orders`
method
will
execute
trades as they
're signaled. When executed,
the
`Trade`
object
will
have
the
order
response
saved
to
it, and the
order
response
will
be
saved
to
a
JSON
file
for further analysis.
    Arguments:
----
trade_obj
{Trade} - - A
trade
object
with the `order` property filled out.
Returns:
----
{dict} - - An
order
response
dicitonary.
"""

# Execute the order.
order_dict = self.session.place_order(
    account=self.trading_account,
    order=trade_obj.order
)

return order_dict

def save_orders(self, order_response_dict: dict) -> bool:
"""
Saves
the
order
to
a
JSON
file
for further review.
    Arguments:
----
order_response
{dict} - - A
single
order
response.
Returns:
----
{bool} - - `True` if the
orders
were
successfully
saved.
"""

# Define the folder.
folder: pathlib.PurePath = pathlib.Path(
    __file__).parents[1].joinpath("data")

# See if it exist, if not create it.
if not folder.exists():
    folder.mkdir()

# Define the file path.
file_path = folder.joinpath('orders.json')

# First check if the file alread exists.
if file_path.exists():
    with open('data/orders.json', 'r') as order_json:
        orders_list = json.load(order_json)
else:
    orders_list = []

# Combine both lists.
orders_list = orders_list + order_response_dict

# Write the new data back.
with open(file='data/orders.json', mode='w+') as order_json:
    json.dump(obj=orders_list, fp=order_json, indent=4)

return True

def get_accounts(self, account_number: str = None, all_accounts: bool = False) -> dict:
"""
Returns
all
the
account
balances
for a specified account.
Keyword
Arguments:
----
account_number
{str} - - The
account
number
you
want
to
query.(default: {None})
all_accounts
{bool} - - Specifies
whether
you
want
to
grab
all
accounts
`True` or not
`False`.(default: {False})
Returns:
----
Dict - - A
dictionary
containing
all
the
information in your
account.
Usage:
----
>> > trading_robot = PyRobot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)
>> > trading_robot_accounts = tradeconsole_session.get_accounts(
    account_number="<YOUR ACCOUNT NUMBER>"
)
>> > trading_robot_accounts
[
    {
        'account_number': 'ACCOUNT_ID',
        'account_type': 'CASH',
        'available_funds': 0.0,
        'buying_power': 0.0,
        'cash_available_for_trading': 0.0,
        'cash_available_for_withdrawl': 0.0,
        'cash_balance': 0.0,
        'day_trading_buying_power': 0.0,
        'long_market_value': 0.0,
        'maintenance_call': 0.0,
        'maintenance_requirement': 0.0,
        'short_balance': 0.0,
        'short_margin_value': 0.0,
        'short_market_value': 0.0
    }
]
"""

# Depending on how the client was initalized, either use the state account
# or the one passed through the function.
if all_accounts:
    account = 'all'
elif self.trading_account:
    account = self.trading_account
else:
    account = account_number

# Grab the accounts.
accounts = self.session.get_accounts(
    account=account
)

# Parse the account info.
accounts_parsed = self._parse_account_balances(
    accounts_response=accounts
)

return accounts_parsed

def _parse_account_balances(self, accounts_response: Union[Dict, List]) -> List[Dict]:
"""
Parses
an
Account
response
into
a
more
simplified
dictionary.
Arguments:
----
accounts_response
{Union[Dict, List]} - - A
response
from the

`get_accounts`
call.
Returns:
----
List[Dict] - - A
list
of
simplified
account
dictionaries.
"""

account_lists = []

if isinstance(accounts_response, dict):

    account_dict = {}

    for account_type_key in accounts_response:

        account_info = accounts_response[account_type_key]

        account_id = account_info['accountId']
        account_type = account_info['type']
        account_current_balances = account_info['currentBalances']
        # account_inital_balances = account_info['initialBalances']

        account_dict['account_number'] = account_id
        account_dict['account_type'] = account_type
        account_dict['cash_balance'] = account_current_balances['cashBalance']
        account_dict['long_market_value'] = account_current_balances['longMarketValue']

        account_dict['cash_available_for_trading'] = account_current_balances.get(
            'cashAvailableForTrading', 0.0
        )
        account_dict['cash_available_for_withdrawl'] = account_current_balances.get(
            'cashAvailableForWithDrawal', 0.0
        )
        account_dict['available_funds'] = account_current_balances.get(
            'availableFunds', 0.0
        )
        account_dict['buying_power'] = account_current_balances.get(
            'buyingPower', 0.0
        )
        account_dict['day_trading_buying_power'] = account_current_balances.get(
            'dayTradingBuyingPower', 0.0
        )
        account_dict['maintenance_call'] = account_current_balances.get(
            'maintenanceCall', 0.0
        )
        account_dict['maintenance_requirement'] = account_current_balances.get(
            'maintenanceRequirement', 0.0
        )

        account_dict['short_balance'] = account_current_balances.get(
            'shortBalance', 0.0
        )
        account_dict['short_market_value'] = account_current_balances.get(
            'shortMarketValue', 0.0
        )
        account_dict['short_margin_value'] = account_current_balances.get(
            'shortMarginValue', 0.0
        )

        account_lists.append(account_dict)

elif isinstance(accounts_response, list):

    for account in accounts_response:

        account_dict = {}

        for account_type_key in account:

            account_info = account[account_type_key]

            account_id = account_info['accountId']
            account_type = account_info['type']
            account_current_balances = account_info['currentBalances']
            # account_inital_balances = account_info['initialBalances']

            account_dict['account_number'] = account_id
            account_dict['account_type'] = account_type
            account_dict['cash_balance'] = account_current_balances['cashBalance']
            account_dict['long_market_value'] = account_current_balances['longMarketValue']

            account_dict['cash_available_for_trading'] = account_current_balances.get(
                'cashAvailableForTrading', 0.0
            )
            account_dict['cash_available_for_withdrawl'] = account_current_balances.get(
                'cashAvailableForWithDrawal', 0.0
            )
            account_dict['available_funds'] = account_current_balances.get(
                'availableFunds', 0.0
            )
            account_dict['buying_power'] = account_current_balances.get(
                'buyingPower', 0.0
            )
            account_dict['day_trading_buying_power'] = account_current_balances.get(
                'dayTradingBuyingPower', 0.0
            )
            account_dict['maintenance_call'] = account_current_balances.get(
                'maintenanceCall', 0.0
            )
            account_dict['maintenance_requirement'] = account_current_balances.get(
                'maintenanceRequirement', 0.0
            )
            account_dict['short_balance'] = account_current_balances.get(
                'shortBalance', 0.0
            )
            account_dict['short_market_value'] = account_current_balances.get(
                'shortMarketValue', 0.0
            )
            account_dict['short_margin_value'] = account_current_balances.get(
                'shortMarginValue', 0.0
            )

            account_lists.append(account_dict)

return account_lists

def get_positions(self, account_number: str = None, all_accounts: bool = False) -> List[Dict]:
"""
Gets
all
the
positions
for a specified account number.
Arguments:
----
account_number(str, optional): The
account
number
of
the
account
you
want
to
pull
positions
for .Defaults to None.
all_accounts(bool, optional): If
you
want
to
return all
the
positions
for every
    account
    then
    set
    to
    `True`.Defaults
    to
    False.
Returns:
----
List[Dict]: A
list
of
Position
objects.
Usage:
----
>> > trading_robot = PyRobot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)
>> > trading_robot_positions = tradeconsole_session.get_positions(
    account_number="<YOUR ACCOUNT NUMBER>"
)
>> > trading_robot_positions
[
    {
        'account_number': '111111111',
        'asset_type': 'EQUITY',
        'average_price': 0.00,
        'current_day_profit_loss': -0.96,
        'current_day_profit_loss_percentage': -5.64,
        'cusip': '565849106',
        'description': '',
        'long_quantity': 3.0,
        'market_value': 16.05,
        'settled_long_quantity': 3.0,
        'settled_short_quantity': 0.0,
        'short_quantity': 0.0,
        'sub_asset_type': '',
        'symbol': 'MRO',
        'type': ''
    },
    {
        'account_number': '111111111',
        'asset_type': 'EQUITY',
        'average_price': 5.60667,
        'current_day_profit_loss': -0.96,
        'current_day_profit_loss_percentage': -5.64,
        'cusip': '565849106',
        'description': '',
        'long_quantity': 3.0,
        'market_value': 16.05,
        'settled_long_quantity': 3.0,
        'settled_short_quantity': 0.0,
        'short_quantity': 0.0,
        'sub_asset_type': '',
        'symbol': 'MRO',
        'type': ''
    }
]
"""

if all_accounts:
    account = 'all'
elif self.trading_account and account_number is None:
    account = self.trading_account
else:
    account = account_number

# Grab the positions.
positions = self.session.get_accounts(
    account=account,
    fields=['positions']
)

# Parse the positions.
positions_parsed = self._parse_account_positions(
    positions_response=positions
)

return positions_parsed

def _parse_account_positions(self, positions_response: Union[List, Dict]) -> List[Dict]:
"""
Parses
the
response
from the

`get_positions`
into
a
more
simplified
list.
Arguments:
----
positions_response
{Union[List, Dict]} - - Either
a
list or a
dictionary
that
represents
a
position.
Returns:
----
List[Dict] - - A
more
simplified
list
of
positions.
"""

positions_lists = []

if isinstance(positions_response, dict):

    position_dict = {}

    for account_type_key in positions_response:

        account_info = positions_response[account_type_key]

        account_id = account_info['accountId']
        positions = account_info['positions']

        for position in positions:
            position_dict['account_number'] = account_id
            position_dict['average_price'] = position['averagePrice']
            position_dict['market_value'] = position['marketValue']
            position_dict['current_day_profit_loss_percentage'] = position['currentDayProfitLossPercentage']
            position_dict['current_day_profit_loss'] = position['currentDayProfitLoss']
            position_dict['long_quantity'] = position['longQuantity']
            position_dict['short_quantity'] = position['shortQuantity']
            position_dict['settled_long_quantity'] = position['settledLongQuantity']
            position_dict['settled_short_quantity'] = position['settledShortQuantity']

            position_dict['symbol'] = position['instrument']['symbol']
            position_dict['cusip'] = position['instrument']['cusip']
            position_dict['asset_type'] = position['instrument']['assetType']
            position_dict['sub_asset_type'] = position['instrument'].get(
                'subAssetType', ""
            )
            position_dict['description'] = position['instrument'].get(
                'description', ""
            )
            position_dict['type'] = position['instrument'].get(
                'type', ""
            )

            positions_lists.append(position_dict)

elif isinstance(positions_response, list):

    for account in positions_response:

        position_dict = {}

        for account_type_key in account:

            account_info = account[account_type_key]

            account_id = account_info['accountId']
            positions = account_info['positions']

            for position in positions:
                position_dict['account_number'] = account_id
                position_dict['average_price'] = position['averagePrice']
                position_dict['market_value'] = position['marketValue']
                position_dict['current_day_profit_loss_percentage'] = position['currentDayProfitLossPercentage']
                position_dict['current_day_profit_loss'] = position['currentDayProfitLoss']
                position_dict['long_quantity'] = position['longQuantity']
                position_dict['short_quantity'] = position['shortQuantity']
                position_dict['settled_long_quantity'] = position['settledLongQuantity']
                position_dict['settled_short_quantity'] = position['settledShortQuantity']

                position_dict['symbol'] = position['instrument']['symbol']
                position_dict['cusip'] = position['instrument']['cusip']
                position_dict['asset_type'] = position['instrument']['assetType']
                position_dict['sub_asset_type'] = position['instrument'].get(
                    'subAssetType', ""
                )
                position_dict['description'] = position['instrument'].get(
                    'description', ""
                )
                position_dict['type'] = position['instrument'].get(
                    'type', ""
                )

                positions_lists.append(position_dict)

return positions_lists











