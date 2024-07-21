import time
from typing import Union

import requests


def take_a_nap(how_many_seconds:Union[int, float]) -> str:
    """Mimic a costly function by just doing nothing for a specified time."""
    time.sleep(float(how_many_seconds))
    return "Rise and shine!"


def check_site_available(url:str, timeout:int=5) -> bool:
    """Checks if a site is available."""
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except requests.RequestException:
        return False


def goofy_wrapper(url:str, timeout:int=5) -> str:
    """Check a site is available, pause for no good reason before summarising
    outcome with a string."""
    msg = f"Napping for {timeout} seconds.\n"
    msg = msg + take_a_nap(timeout)
    if check_site_available(url):
        msg = msg + "\nYour site is up!"
    else:
        msg = msg + "\nYour site is down!"

    return msg
