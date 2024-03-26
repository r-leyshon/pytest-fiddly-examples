"""Helping learners understand how to work with pytest fixtures."""
import pandas as pd


def serve_food(df: pd.DataFrame) -> pd.DataFrame:
    """Serve characters their desired food.

    Iterates over a df, feeding characters if they have 'the munchies' with
    their fave_food. If the character is not Scooby Doo or Shaggy, then update
    their has_munchies status to False. The input df is modified inplace.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe with the following columns: "name": str, "fave_food": str,
        "has_munchies": bool, "stomach_contents": str.

    Returns
    -------
    pd.DataFrame
        Updated dataframe with new statuses for stomach_contents and
        has_munchies.

    """
    for ind, row in df.iterrows():
        if row["has_munchies"]:
            # if character is hungry then feed them
            food = row["fave_food"]
            character = row["name"]
            print(f"Feeding {food} to {character}.")
            df.loc[ind, ["stomach_contents"]] = food
            if character not in ["Scooby Doo", "Shaggy"]:
                # Scooby & Shaggy are always hungry
                df.loc[ind, "has_munchies"] = False
        else:
            # if not hungry then do not adjust
            pass
    return df


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
