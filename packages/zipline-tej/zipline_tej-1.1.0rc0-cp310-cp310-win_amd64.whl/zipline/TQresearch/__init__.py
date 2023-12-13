"""
Zipline research API.

The functions in this module are most often used in a Jupyter notebook, outside
of the context of a Zipline algorithm. For the Zipline algorithm API, see the
`zipline.api` module.

Functions
---------
use_bundle
    Temporarily set the default bundle to use for subsequent research calls.

run_pipeline
    Execute a pipeline.

get_forward_returns
    Get forward returns for the dates and assets in an input factor (typically
    the output of `run_pipeline`).

get_data
    Return a `zipline.api.BarData` object for a specified bundle and datetime.

sid
    Lookup an Asset by its unique sid.

symbol
    Lookup an Equity by its ticker symbol.

continuous_future
    Return a `zipline.assets.ContinuousFuture` object for a specified root symbol.

Notes
-----
Usage Guide:

* Research API: https://qrok.it/dl/z/zipline-research
"""
from zipline.TQresearch.tej_pipeline import run_pipeline #, get_forward_returns
# from zipline.TQresearch.bundle import use_bundle
# from zipline.TQresearch.bardata import get_data
# from zipline.TQresearch import sid as sid_module # for test suite
# from zipline.TQresearch.sid import sid, symbol
# from zipline.TQresearch import continuous_future as continuous_future_module # for test suite
# from zipline.TQresearch.continuous_future import continuous_future

__all__ = [
    # 'use_bundle',s
    'run_pipeline',
    # 'get_forward_returns',
    # 'get_data',
    'sid',
    'symbol',
    'continuous_future',
]