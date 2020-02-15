
# coding: utf-8

# In[1]:


import requests 
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


# In[2]:


with open('/home/pi/snowmap/snowmap/data.json') as f:
    response = json.load(f)


# In[3]:


vehiclejson = requests.get("https://api.networkfleet.com/vehicles/devicemodel?in-group=434774",
                       headers={'Authorization': "Bearer "+response['access_token'],
                                'Accept': "application/vnd.networkfleet.api-v1+json",
                                'Content-Type': "application/vnd.networkfleet.api-v1+json"}
                      ).json()


# In[4]:


vehiclejsondf = pd.DataFrame(vehiclejson)


# In[5]:


vehiclelist = pd.io.json.json_normalize(vehiclejsondf['vehicle'])


# In[6]:


vehiclelist = vehiclelist['@id'].astype(str)

#vehiclelist = vehiclelist[['@id', 'model', 'label']].astype(str)
# In[7]:


vehicleLabel = pd.io.json.json_normalize(vehiclejsondf['vehicle'])[['@id', 'label']]


# In[10]:


with open('/home/pi/snowmap/snowmap/vehicleLabel.txt', 'w') as filehandle:
    for listitem in vehiclelist:
        filehandle.write('%s\n' % listitem)

