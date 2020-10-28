""" This module contains functions to perform data validation on a dataframe"""

import pandas as pd
from datetime import datetime
from typing import List

def validate(df: pd.DataFrame)-> bool:
    """
    Assumes that df is a Pandas dataframe. 
    Returns True if dataframe follows  the following criteria:
    - Contains 6 columns
    - No value in the dataframe is undefined 
    - First columnn has integers corresponding to valid latitudes
    - Second column has integers corresponding to valid longitudes
    - Fourth Column has values that can be interpreted as dates

    If any of these requirements are not met an exception is 
    raised indicating the problem. 
    """
    
    if len(df.columns) != 6:
        raise ValueError("You must have exactly six columns in your data")
        
    if df.isnull().values.any():
        raise ValueError("Some entries in data are empty")

    if not are_valid_coord(list(df.iloc[:,0])):
        error_msg = "Entries in the first column must represent valid longitudes."
        raise ValueError(error_msg)

    if not are_valid_coord(list(df.iloc[:,1])):
        error_msg = "Entries in the second column must represent valid latitudes."
        raise ValueError(error_msg)
    
    if not are_valid_dates(list(df.iloc[:,3])):
        error_msg = "Entries in the fourth column must represent valid dates."



def are_valid_coord(arr: List[str]) -> bool:
    """ Assumes that arr is list of strings or integers
    Returns True if every value in the list can be converted 
    to a number between -90 and 90. Returns False otherwise."""
    for elem in arr:
        try: 
            num = float(elem)
            if num > 90 or num < -90:
                return False
        except Exception:
            return False
    return True

def are_valid_dates(arr: List[str])->bool:
    """TODO: This is curently a placeholder method to check 
    whether the array contains valid datetimes.
    Assumes: arr is a list of strings
    Returns: True if every string is in format 'month/day/year' """
    return True

        





                       


