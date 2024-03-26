"""A module containing an expensive class definition."""
import time
from typing import Union


class ExpensiveDoodah:
    """A toy class that represents some costly operation.

    Parameters
    ----------
    sleep_time : Union[int, float]
        Number of seconds to wait on init.

    """

    def __init__(self, sleep_time: Union[int, float] = 2):
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)
        return None
