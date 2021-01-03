import os
import numpy as np
import json
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from IPython.display import HTML
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from getpass import getpass
from shapely.geometry import MultiPolygon, Polygon
from geojson import Polygon
import rasterio as rio
from rasterio.plot import show
import rasterio.mask
import fiona
import folium

AREA = [[-123.293536, 49.362603],
        [-123.293536, 49.005211],
        [-122.74628, 49.005211],
        [-122.74628, 49.362603],
        [-123.293536, 49.362603]]

m = Polygon([AREA])

object_name = "Vancouver"
with open(object_name + ".geojson", 'w') as f:
    json.dump(m, f)
footprint_geojson = geojson_to_wkt(read_geojson(object_name + ".geojson"))

user = input("USER NAME: ")
password = getpass("PASSWORD: ")
api = SentinelAPI(user, password, "https://scihub.copernicus.eu/dhus")

m = folium.Map([(AREA[0][1] + AREA[len(AREA)-1][1])/2, (AREA[0][0] + AREA[len(AREA)-1][0])/2], zoom_start=10)
folium.GeoJson(object_name + '.geojson').add_to(m)
m.save(outfile="datamap.html")
# os.system('open datamap.html')

products = api.query(footprint_geojson,
                     date = ('20201201', '20201221'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 100))

products_gdf = api.to_geodataframe(products)
products_gdf_sorted = products_gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
products_gdf_sorted