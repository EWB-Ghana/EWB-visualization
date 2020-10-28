from ewb_mappy.validation import validate

import re
import pandas as pd 

CSV_EXTENSION  = 'csv'
EXCEL_EXTENSION = 'xls'



class Map():
    """
    Object to reprent map
    Attributes: 
    - df: Dataframe with data
    """

    def __init__(self):
        df = None



def determine_extension(filename: str) -> str:
    """
    Returns type of extension constant  associated with a Filename.
    If Extension is not supperted IOError is raised.
    """
    name_pattern = r'.*'
    excel_reg = re.compile(name_pattern + r'.(xls|xlsx|xlsm|xlsb|xls)$')
    csv_reg = re.compile(name_pattern + r'.csv$')
    extension = None
        
    if excel_reg.match(filename):
        extension = EXCEL_EXTENSION
    elif csv_reg.match(filename):
        extension = CSV_EXTENSION
    else:
        error_msg = "File extension or name of " + filename
        error_msg += " not supported. Use csv or excel documents"
        raise IOError(error_msg)
    
    return extension

    
def get_dataframe(filename: str) -> pd.DataFrame:
    """
    Returns a dataframe from an excel or csv file
    """
    
    extension = determine_extension(filename)
    df = None
    if extension == EXCEL_EXTENSION:
        df = pd.read_excel(filename)
    elif extension == CSV_EXTENSION:
        df = pd.read_csv(filename)

    return df


def get_map(filename: str) -> Map:
    """"
    Returns a map object read from a csv or excel file
    """

    map_object = Map()
    map_object.df = get_dataframe(filename)
    validate(map_object.df)
    return map_object
        




    
    
