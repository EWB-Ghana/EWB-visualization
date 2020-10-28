# popups.py
#
# This program creates comprehensive popups for each datapoint in the input map layer,
# using information such as title, date, and description from the spreadsheet.
# 
# VARIABLES
# CSV filename: 'mapdata.csv'
# Excel filename: 'mapdata.xlsx'
# spreadsheet: 'load'
# sheet: 'layer'
# row in spreadsheet (datapoint): 'landmark'
# map object: 'map'
# latitude of point: 'lat'
# longitude of point: 'lon'
# title of point: 'title'
# date of entry: 'date'
# point description: 'description'
# layer icon: 'icon' (https://fontawesome.com/icons?d=gallery)
# layer color: 'color'

import pandas
import folium

# add markers with descriptive popups for each landmark in the layer
def make_popups(map, lat, lon, title, date, description, icon, color):
    """
    Adds a popup with the specified information & styling attributes to the data layer
    at the geographical location dictated by the latitude and longitude coordinates.
    
    Parameters
    ----------
    map : Map (folium)
        map to be displayed
    lat : float
        latitude coordinate (decimal notation)
    lon : float
        longitude coordinate (decimal notation)
    title : string
        name of the datapoint (to be displayed by the tooltip)
    date : string
        date associated with the datapoint
    description : string
        description of the datapoint
    icon : string
        icon to be displayed in the popup pin
    color : string
        color of the popup pin
    """
    folium.Marker(
        location = [lat, lon],
        icon = folium.Icon(icon=icon, color=color),
        tooltip = title,
        popup = folium.Popup(
            folium.Html('<b>%s</b> <br> <i>%s</i> <br> %s' %(title, date, description), script=True),
            min_width=100,
            max_width=450
            )
    ).add_to(map)

# Excel:
load = pandas.ExcelFile('mapdata.xlsx')

for name in load.sheet_names:
    layer = load.parse(name)

    if 'icon' in layer.columns:
        icon = layer['icon'].iloc[0]
    else:
        icon = 'tint'

    if 'color' in layer.columns:
        color = layer['color'].iloc[0]
    else:
        color = 'blue'

    for landmark in layer.itertuples():
        make_popups(
            map=map,
            lat=landmark.lat,
            lon=landmark.lon,
            title=landmark.title,
            date=landmark.date,
            description=landmark.description,
            icon=icon,
            color=color
        )

# CSV:
layer = pandas.read_csv('mapdata.csv')

if 'icon' in layer.columns:
    icon = layer['icon'].iloc[0]
else:
    icon = 'tint'

if 'color' in layer.columns:
    color = layer['color'].iloc[0]
else:
    color = 'blue'

for landmark in layer.itertuples():
    make_popups(
            map=map,
            lat=landmark.lat,
            lon=landmark.lon,
            title=landmark.title,
            date=landmark.date,
            description=landmark.description,
            icon=icon,
            color=color
        )
