# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:35:49 2020

@author: Stan
"""

import os
import folium
from folium import FeatureGroup, LayerControl, Map, Marker
import time
import datetime
import re
import pandas as pd 

CSV_EXTENSION  = 'csv'
EXCEL_EXTENSION = 'xls'

# NOTE:
# TO-DO
# 1. test your functions
# 2. add docstrings --> check PEP8/google python docstring conventions
#      # minimum requirement:
#      # inputs and types, functions, return types
# 3. after you finish 1 & 2, put all your functions in master/EWBMappy/your_name.py

# Jannie
class EWBLayer():
    """
    A class to represent a layer on the map.
    ...

    Attributes
    ----------
    name : str
        name of the layer
    color : str
        color of the layer
    df : dataframe
        dataframe containing the data of the layer
    points : array
        array containing tuples of coordinate points of the layer
    featureGroup : FeatureGroup
        represents a group of points on the map
        
    Methods
    -------
    None

    """
    def __init__(self, name, color, df):
        """
        Constructs all the necessary attributes for the EWBLayer object.

        Parameters
        ----------
        name : str
            name of the layer
        color : str
            color of the layer
        df : dataframe
            dataframe containing the data of the layer
            
        """
        self.name = name
        self.color = color
        self.df = df
        self.points = []
        self.featureGroup = FeatureGroup(name=name)

# ref: https://github.com/python-visualization/folium/issues/460
class EWBMap():
    """
    A class to represent the entire folium map.
    ...

    Attributes
    ----------
    layers : array
        array of all layers to be shown on this map
    map : Map (folium)
        map to be displayed
    layerNames : array
        list of names of layers in the map
    
    Methods
    -------
    makeMapfromLayers():
        Creates a map from the existing layers.
    recenter(string="all"):
        Recenter the map around the given points.

    """
    
    # Jannie
    def __init__(self):
        """
        Constructs all the necessary attributes for the EWBMap object.

        Parameters
        ----------
        None
        
        """
        self.layers = []
        self.map = Map(
            location=[45.372, -121.6972],
            zoom_start=12,
            tiles='Stamen Terrain'
        )
        listOfTiles = ['Stamen Toner', 'openstreetmap']
        for tile in listOfTiles:
            folium.TileLayer(tile).add_to(self.map) 
        self.layerNames = []
    # Jannie
    def makeMapfromLayers(self):
        for layer in self.layers:
            layer.featureGroup.add_to(self.map)
        folium.LayerControl().add_to(self.map)
    # Chen
    def recenter(self, string = "all"):
        # center around the town - hardcode location TBD
        if string == 'town':
            x = 45.5236
            y = -122.6750
            self.map.location = [x, y]

        elif string in self.layerNames:
            xMin, xMax, yMin, yMax = [100, -100, 181, -181]
            idx = self.layerNames.index(string)
            layer = self.layers[idx]
            # layer.df[0] - latitutde, layer.df[1] - longitude --> I know this looks ugly
            # but is only meant to be a quick fix, will be optimized later
            xMin = min(xMin, min(layer.df.iloc[:,0]))
            xMax = max(xMax, max(layer.df.iloc[:,0]))
            yMin = min(yMin, min(layer.df.iloc[:,1]))
            yMax = max(yMax, max(layer.df.iloc[:,1]))
            # adjust the map bound according the upper and lower bound of the dataset
            self.map.fit_bounds([[xMin, yMin], [xMax, yMax]])
        
        elif string == 'all':
            xMin, xMax, yMin, yMax = [100, -100, 181, -181]
            for layer in self.layers:
                xMin = min(xMin, min(layer.df.iloc[:,0]))
                xMax = max(xMax, max(layer.df.iloc[:,0]))
                yMin = min(yMin, min(layer.df.iloc[:,1]))
                yMax = max(yMax, max(layer.df.iloc[:,1]))
            # adjust the map bound according the upper and lower bound of the dataset
            self.map.fit_bounds([[xMin, yMin], [xMax, yMax]])
        # if the input string does not match any of the options
        else:
            print(f"ERROR: wrong string input: {string}\n, valid inputs are: {self.layerNames} or 'all' or 'town")

# Nicolas
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

# Nicolas
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
    else:
        error_msg = "File extension or name of " + filename
        error_msg += " not supported. Use csv or excel documents"
        raise IOError(error_msg)
    # doing validation, modification, and dataframe making at the same time
    # could be a terribly bad idea but a quick fix for now --Chen
    for i in range(df.shape[0]):
        for j in range(2):
            string = df.iloc[i, j]
            if type(string) == str and '°' in string:
                df.iloc[i,j] = conv_coord(string)
    return df

# Toby
def conv_coord(deg_notation):
    degrees, rest = deg_notation.split('°', 1)
    minutes, rest = rest.split("'", 1)
    seconds, direction = rest.split('"', 1)
    dec_notation = float(degrees) + float(minutes)/60 + float(seconds)/3600
    
    if direction == 'S' or direction == 'W':
        dec_notation = -dec_notation

    return dec_notation

# Nicolas
def get_map(files: list) -> EWBMap:
    """"
    Returns a map object read from a csv or excel file
    """
    map_object = EWBMap()
    for f in files:
        layer = get_layer(f)
        map_object.layers.append(layer)
        map_object.layerNames.append(layer.name)
    map_object.makeMapfromLayers()
    map_object.recenter()
    return map_object

# Chen
def get_layer(filename: str) -> EWBLayer:
    map_df = get_dataframe(filename)
    layername, color, _= re.split(',|_|-|\\.',filename.replace(' ', ''))
    layer_object = EWBLayer(layername, color, map_df)

    for row in map_df.itertuples():
        tmpRow = list(row)
        make_popups(layer_object.featureGroup, tmpRow[1], tmpRow[2], tmpRow[3], 
                    tmpRow[4], tmpRow[5], tmpRow[6], layer_object.color)

    return layer_object
   
# Toby
def make_popups(layer, lat, lon, title, date="", description="", icon="home", color="lightgray"):
    if date == "":
        date = datetime.datetime.now()
    folium.Marker(
        location = [lat, lon],
        icon = folium.Icon(icon=icon, color=color, prefix='fa'),
        tooltip = title,
        popup = folium.Popup(
                    folium.Html('<b>%s</b> <br> <i>%s</i> <br> %s' %(title, date, description), script=True),
                    # min_width=100,=> this is no longer valid
                    max_width=450)
        ).add_to(layer)
    
    
# Danny (--> there is another data validation function not uploaded to this notebook to test too)
def map_to_html (m, map_name, file_path =""):
    if file_path != "" and file_path[-1]!= '/':
        file_path = file_path+"/"
    path = file_path+map_name+".html"
    m.save(path)
    return path

# still not working :/
# we will not continue developing this function, I only keep this here for record keeping. --Chen
def map_to_png(m, map_name, file_path ="", browser= 'Chrome'):
    if file_path != "" and file_path[-1]!= '/':
        file_path = file_path+"/"
    fn = map_name+".html"
    m.save(fn)
    tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
    delay =5
    if browser == 'Safari':
        browser = webdriver.Safari()
    elif browser == 'Firefox':
        browser = webdriver.Firefox()
    else:
        browser = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.binary_location = "./chromedriver.exe"    #chrome binary location specified here
    options.add_argument("--start-maximized") #open Browser in maximized mode
    options.add_argument("--no-sandbox") #bypass OS security model
    options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    brower = webdriver.Chrome(options=options, executable_path=r'./chromedriver.exe')
    # browser.get('http://google.com/')
    
    browser.get(tmpurl)
    # time.sleep(delay)
    # browser.save_screenshot(file_path+map_name+'.png')
    # browser.quit()
