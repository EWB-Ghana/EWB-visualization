# Chen
    """
	input: string indicating the layer to center the map on, optional, default = "all"
	output: none
	functionality: auto-center the map at the centroid of all points on designated layers
	"""
    def recenter(self, string = "all"):
        # center around the town - hardcode location TBD
        if string == 'town':
            x = 45.5236
            y = -122.6750
            self.map.location = [x, y]
        # center based on point on a specific layer
        elif string in self.layerNames:
            xMin, xMax, yMin, yMax = [100, -100, 181, -181]
            idx = self.layerNames.index(string)
            layer = self.layers[idx]
            # layer.df[0] - latitutde, layer.df[1] - longitude
            lat = layer.df.iloc[:,0]
            lon = layer.df.iloc[:,1]
            xMin = min(xMin, min(lat))
            xMax = max(xMax, max(lat))
            yMin = min(yMin, min(lon))
            yMax = max(yMax, max(lon))
            # adjust the map bound according the upper and lower bound of the dataset
            self.map.fit_bounds([[xMin, yMin], [xMax, yMax]])
        
        elif string == 'all':
            xMin, xMax, yMin, yMax = [100, -100, 181, -181]
            for layer in self.layers:
            	lat = layer.df.iloc[:,0]
            	lon = layer.df.iloc[:,1]
            	xMin = min(xMin, min(lat))
            	xMax = max(xMax, max(lat))
            	yMin = min(yMin, min(lon))
            	yMax = max(yMax, max(lon))
            # adjust the map bound according the upper and lower bound of the dataset
            self.map.fit_bounds([[xMin, yMin], [xMax, yMax]])
        # if the input string does not match any of the options
        else:
            raise IOError(f"ERROR: wrong string input: {string}\n, valid inputs are: {self.layerNames} or 'all' or 'town")


# Chen
"""
input:path to the file with layer information in csv/xlsx format, e.g. 'name_of_layer,color_of_layer.xlsx'
        note that the name_of_layer should not contain comma
output:a EWBLayer object aggregating layer information, which will in turn be processed by get_map
functionality: process excel/csv information into folium layer
"""
def get_layer(filename: str) -> EWBLayer:
    map_df = get_dataframe(filename)
    name = re.split('/', filename)[-1]
    output = re.split(',|\\.',name.replace(' ', ''))
    if len(output) != 3:
        raise ValueError(f"The filename should be <layer name>,<layer color>.csv/xlsx, received filename {name}")
    layername, color, _ = output
    color = color.lower()
    layer_object = EWBLayer(layername, color, map_df)

    for row in map_df.itertuples():
        tmpRow = list(row)
        make_popups(layer_object.featureGroup, tmpRow[1], tmpRow[2], tmpRow[3], 
                    tmpRow[4], tmpRow[5], tmpRow[6], layer_object.color)

    return layer_object