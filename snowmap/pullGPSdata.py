# coding: utf-8

# In[173]:


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
import re
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap/snowmap/snowmap')

# In[136]:


with open('data.json') as f:
    response = json.load(f)


# In[168]:




# In[170]:


with open('vehicleLabel.txt', 'r') as f:
    vehicles = f.readlines()


# In[178]:


#plowed_last_hour,plowed_total,not_plowed,time
#1409,1804,3767,2019-12-17 05:00:00


snowice = [
"977624",
"966199",
"975119",
"951170",
"1036576",
"952216",
"952883",
"975118",
"951625",
"954047",
"952406",
"940427",
"952150",
"952315",
"954287",
"954281",
"951074",
"954050",
"971650",
"967230",
"966223",
"966236",
"966474",
"955397",
"970771",
"973265",
"953696",
"954279",
"973267",
"950063",
"973261",
"938761",
"952387",
"977159",
"987971",
"977106",
"977331",
"988791",
"977157",
"988604",
"1049354"]



vehicles = [item.replace("\n", "") for item in vehicles]
#vehicles = [int(x) for x in vehicles]

# In[137]:


timezone = timedelta(hours = 4)
#systime = datetime.now() + timezone - timedelta(hours = 1)
#currenthour = (systime - timezone).hour
#date = (systime - timezone).strftime('%Y-%m-%d')
#start_date = systime.strftime("%Y-%m-%dT%H") + ':00:00Z'
#end_date = systime.strftime("%Y-%m-%dT%H") + ':59:59Z'


# In[147]:


systime = datetime.now() + timezone
start_date = (systime - timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")


# In[144]:


end_date = systime.strftime("%Y-%m-%dT%H:%M:%SZ")


# In[145]:


#appended_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
gps_data = pd.read_csv("gps_data.csv")
appended_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
# In[146]:


for i in vehicles:
    try:
        rjson = requests.get("https://api.networkfleet.com/locations/vehicle/"+i+"/track?limit=240&with-start-date="+start_date+"&with-end-date="+end_date,
                       headers={'Authorization': "Bearer "+response['access_token'],
                                'Accept': "application/vnd.networkfleet.api-v1+json",
                                'Content-Type': "application/vnd.networkfleet.api-v1+json"}
                      ).json()

        if rjson['count'] != 0:
            jsondf = pd.DataFrame(rjson)
            gpsMessage = pd.io.json.json_normalize(jsondf['gpsMessage'])
            gpsMessage_filter = gpsMessage[['latitude', 'longitude', 'messageTime', 'odometer.value']]
            gpsMessage_filter['truck_name'] = i
            gpsMessage_filter['timeedit'] = pd.to_datetime(gpsMessage_filter['messageTime'])
            #Nameedit['hour'] = (Nameedit["timeedit"]-timezone).dt.hour
            gpsMessage_filter['datetime'] = (gpsMessage_filter['timeedit']-timezone).dt.strftime("%Y-%m-%d %H:00:00")
            gpsMessage_filter['longitude'] = gpsMessage_filter.longitude.round(6)
            gpsMessage_filter['latitude'] = gpsMessage_filter.latitude.round(6)
            gpsMessage_filter = gpsMessage_filter[['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime']]
            appended_data = gpsMessage_filter.append(appended_data)
            print("success: "+ i)
        else:
            print("0 count: " +i)

    except:
        print ("fail: " + i)

gps_data = gps_data.append(appended_data)
# In[150]:


gps_data.to_csv("gps_data.csv", index = False)
