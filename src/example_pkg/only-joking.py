"""Retrieve dad jokes available."""
from typing import Union

import requests

def get_joke(f:Union[str, None]=None):
    ENDPOINT = "https://icanhazdadjoke.com/"
    HEADERS = {
        "User-Agent": "datasavvycorner.com (https://github.com/r-leyshon/pytest-fiddly-examples)",
        "Accept": f,
        # "Accept": "application/json"
        # "Accept": "text/plain"

        }
    resp = requests.get(ENDPOINT, headers=HEADERS)
    if resp.ok:
        if HEADERS["Accept"] == "application/json":
            content = resp.json()
            content = content["joke"]
        elif HEADERS["Accept"] == "text/plain":
            content = resp.content
        else:
            raise NotImplementedError(
                "This client only accepts 'application/json' or 'text/plain' format"
                )
    else:
        raise requests.HTTPError(
            f"{resp.status_code}: {resp.reason}"
        )
    return content


get_joke()
get_joke(f="application/json")
type(get_joke(f="text/plain"))

