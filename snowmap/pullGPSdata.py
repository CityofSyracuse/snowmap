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
"1049354",
"980027",
"970775",
"977157",
"973267",
"977624",
"973265",
"1107444",
"938761",
"940427",
"950063",
"951170",
"952150",
"1110487",
"952315",
"1111119",
"954287",
"1112291",
"1098568",
"952883",
"952406",
"955411",
"953696",
"952080",
"966223",
"970771",
"951625",
"987971",
"952387",
"952216",
"975118",
"977159",
"977106",
"1080281",
"957144",
"1110736",
"1110490",
"977331",
"1110489",
"1110735",
"955397",
"975119",
"954281",
"954050",
"954047",
"988791",
"966474",
"982178",
"951074",
"971587",
"951655",
"970736",
"1016105",
"988584",
"1036576",
"966236",
"967230",
"988604",
"960635",
"971650",
"973261",
"955921",
"966199",
"954279",
"967335",
"966197",
"955536",
"954285",
"1098937",
"1067585",
"952096",
"952082",
"952081",
"952099",
"972989",
"952101",
"952074",
"1075062",
"1077056",
"1068399",
"1068397",
"1067876",
"1068404"
]



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
start_date = (systime - timedelta(minutes=20160)).strftime("%Y-%m-%dT%H:%M:%SZ")


# In[144]:


end_date = systime.strftime("%Y-%m-%dT%H:%M:%SZ")


# In[145]:


#appended_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
gps_data = pd.read_csv("gps_data.csv")
appended_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
# In[146]:


for i in vehicles:
    try:
        rjson = requests.get("https://api.networkfleet.com/locations/vehicle/"+i+"/track?limit=6000&with-start-date="+start_date+"&with-end-date="+end_date,
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
