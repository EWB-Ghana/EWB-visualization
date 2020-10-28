import folium

# default csv file headers:
# xCoord, yCoord, message, style, tooltip, (iconShape, iconColor)

# add markers to map
def addToMap(map, location, message, style='i', tootltip = ""):
    # if single marker addition and not wrapped in list
    if (type(message) is str):
        if (type(style) is str):
            key = style
        else:
            key = style[0]
        msg_str = f'<{key}>'+message+f'</{key}>'
        folium.Marker(location, popup=msg_str, tooltip=tooltip).add_to(map)
        return map
    # if adding multiple markers at the same time
    elif type(message) is list:
        for msg in enumerate(message):
            if (type(style) is str):
                key = style
            else:
                key = style[msg[0]]
            msg_str = f'<{key}>'+message+f'</{key}>'
            loc = location[msg[0]]
            folium.Marker(loc, popup=msg_str, tooltip=tooltip).add_to(map)
        return map

# pass in the map to re-center around fixed point
def recenter(map, string, ptsList=[]):
    # center around the town
    if string == 'town':
        x = 45.5236
        y = -122.6750
        map.location = [x, y]
    # ghana: show all datapoints in EWB-Ghana
    # all-ewb: show transportation and overview of all EWB project location
    elif string == 'ghana' or string == 'all-ewb':
        # if input location list is empty
        if len(ptsList)<1:
            print("ERROR: list input is empty")
        else:
            # find the SW and NE bound of the dataset
            first = ptsList[0]
            xMin = first[0]
            yMin = first[1]
            xMax = xMin
            yMax = yMin
            for pt in ptsList:
                xMin = min(xMin, pt[0])
                xMax = max(xMax, pt[0])
                yMin = min(yMin, pt[1])
                yMax = max(yMax, pt[1])
            # adjust the map bound according the upper and lower bound of the dataset
            map.fit_bounds([[xMin, yMin], [xMax, yMax]])
    # if the input string does not match any of the options
    else:
        print("ERROR: wrong string input")
    return map
    