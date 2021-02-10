import requests
import traceback
from time import gmtime, strftime
import time as t
import pandas as pd
from shapely.geometry import shape, Point
from pyproj import Proj, transform
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import shapely
import folium
from datetime import *
import numpy as np
import json
import io
import requests
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap/snowmap')

dataSrc = gpd.read_file('dataSrc.geojson')

dataSrc = dataSrc[(dataSrc['CART_TYPE'] != 'INTERSTATES') & (dataSrc['CART_TYPE']!='RAMPS') & (dataSrc['CART_TYPE']!='PEDESTRIAN') &
        (dataSrc['CART_OWN']!="PRIVATE")&
        (~dataSrc['STREET'].isin(['FARMERS MARKET WAY' , 'NBT BANK PKWY' , 'DESTINY USA SERVICE RD', 'DESTINY USA TO SB I 81 RAMP', 'DESTINY USA FROM SB I 81 RAMP', 'DESTINY USA DR'])) &
        (~dataSrc['STREET_ID'].isin([13020737,12572689,13013383,13013382,13013377,13013381,13013380,12572623,12572620,13013389,13021028,13013390,12572506,12572503,13013391,12572501,12572508,12572525,12572526,12572664,12572659,13028975,13001278,13001275,13001277,13008682,13001274,12574889,12574981,13028975]))
       ]


c=pd.read_csv('gps_data.csv')

geometry = [Point(xy) for xy in zip(c.longitude, c.latitude)]

Nameedit1 = GeoDataFrame(c, geometry=geometry)

Nameedit1 = GeoDataFrame(Nameedit1, geometry='geometry')

Nameedit1.crs = 'EPSG:4326'

x1 = gpd.sjoin(Nameedit1, dataSrc, op='intersects')

x1 = x1[['STREET_ID', 'datetime']]
res = x1.groupby('STREET_ID')['datetime'].max().reset_index()

mergeddata_all = dataSrc[['STREET', 'geometry', 'STREET_ID']].merge(res, left_on='STREET_ID', right_on='STREET_ID', how='right')

mergeddata = mergeddata_all[mergeddata_all['datetime'] == mergeddata_all["datetime"].max()]

notplowed = dataSrc[(~dataSrc['STREET_ID'].isin(mergeddata_all['STREET_ID'].astype(object)))]

with open('mergeddata.geojson', 'w') as f:
    f.write(mergeddata_all.to_json())


with open('last_hour.geojson', 'w') as f:
    f.write(mergeddata.to_json())

with open('notplowed.geojson', 'w') as f:
    f.write(notplowed.to_json())
