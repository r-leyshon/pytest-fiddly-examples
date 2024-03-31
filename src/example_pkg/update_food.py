"""Helping learners understand how to work with pytest fixtures."""
import pandas as pd


def fancy_dessert(
    df: pd.DataFrame,
    fave_desserts: dict = {
        "Daphne": "brownie",
        "Fred": "ice cream",
        "Scooby Doo": "apple crumble",
        "Shaggy": "pudding",
        "Velma": "banana bread",
    },
) -> pd.DataFrame:
    """Update a characters favourite_food to a dessert if they have eaten.

    Iterates over a df, updating the fave_food value for a character if the
    stomach_contents are not 'empty'.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe with the following columns: "name": str, "fave_food": str,
        "has_munchies": bool, "stomach_contents": str.
    fave_desserts : dict, optional
        A mapping of "name" to a replacement favourite_food, by default
        { "Daphne": "brownie", "Fred": "ice cream",
        "Scooby Doo": "apple crumble", "Shaggy": "pudding",
        "Velma": "banana bread", }

    Returns
    -------
    pd.DataFrame
        Dataframe with updated fave_food values.

    """
    for ind, row in df.iterrows():
        if row["stomach_contents"] != "empty":
            # character has eaten, now they should prefer a dessert
            character = row["name"]
            dessert = fave_desserts[character]
            print(f"{character} now wants {dessert}.")
            df.loc[ind, "fave_food"] = dessert
        else:
            # if not eaten, do not adjust
            pass
    return df
