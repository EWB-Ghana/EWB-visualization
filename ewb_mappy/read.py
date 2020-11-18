from ewb_mappy.validation import validate

import re
import pandas as pd
import os

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


def get_map(files: list) -> EWBMap:
    """"
    Returns a map object with layers as specified in files
    """
    
    map_object = EWBMap()
    for f in files:
        layer = getlayer(f)
        map_object.layers.append(layer)
        map_object.layerNames.append(layer.name)
    map_object.makeMapfromLayers()
    map_object.recenter()
    return map_object
        

def get_layers(filename: str) -> EWBLayer:
    """
    Function that returns an EWBLayer from filename. 
    Extensions can be csv or can be excel. 
    Color of the layer must be specified in the file
    """

    #TODO find a better way to deal with colors
    layer_df = get_dataframe(filename)
    color = 'lightgray'
    layername = os.path.splitext(filename)[0]
    layer_object = EWB(layername, color, layerdf)
    for row in layer_df.itertuples():
        tmpRow = list(row)
        #TODO remember to change this 
        layer_object.make_popups(lat=tmpRow[1],
                                 lon=tmpRow[2],
                                 title=tmpRow[3],
                                 date=tmpRow[4],
                                 description=tmpRow[5],
                                 icon=tmpRow[6])
        



    
    
