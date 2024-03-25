"""Helping learners understand how to work with pytest fixtures.

These functions work with a dataframe with the following schema:
"name": str,
"fave_food": str,
"has_munchies": bool,
"stomach_contents": str,
"""
import pandas as pd
import numpy as np


def serve_food(df:pd.DataFrame) -> pd.DataFrame:
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


def update_food(
    df:pd.DataFrame,
    fave_desserts:dict={
        "Daphne": "brownie",
        "Fred": "ice cream",
        "Scooby Doo": "apple crumble",
        "Shaggy": "pudding",
        "Velma": "banana bread",
        }) -> pd.DataFrame:
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
