


# coding: utf-8

# In[1013]:


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
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap')


# In[1054]:


with open('data.json') as f:
    response = json.load(f)


# In[1055]:


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


# In[1016]:


dataSrc = gpd.read_file('dataSrc.geojson')


# In[1017]:


dataSrc = dataSrc[(dataSrc['CART_TYPE'] != 'INTERSTATES') & (dataSrc['CART_TYPE']!='RAMPS') & (dataSrc['CART_TYPE']!='PEDESTRIAN') &
        (dataSrc['CART_OWN']!="PRIVATE") &
        (~dataSrc['STREET'].isin(['FARMERS MARKET WAY' , 'NBT BANK PKWY' , 'DESTINY USA SERVICE RD', 'DESTINY USA TO SB I 81 RAMP', 'DESTINY USA FROM SB I 81 RAMP', 'DESTINY USA DR'])) &
        (~dataSrc['STREET_ID'].isin([13020737,12572689,13013383,13013382,13013377,13013381,
	13013380,12572623,12572620,13013389,13021028,13013390,12572506,12572503,13013391,
	12572501,12572508,12572525,12572526,12572664,12572659,13028975,13001278,13001275,13001277,13008682,13001274,12574889,12574981,13028975]))
       ]


# In[1056]:


#mergeddata_all = gpd.read_file('/home/pi/snowmap/snowmap/mergeddata.geojson')


# In[1057]:


#mergeddata_all['datetime'] = pd.to_datetime(mergeddata_all['datetime'])


# In[1058]:


timezone = timedelta(hours = 5)
systime = datetime.utcnow() - timedelta(hours=1)
#currenthour = (systime - timezone).hour
#date = (systime - timezone).strftime('%Y-%m-%d')
start_date = systime.strftime("%Y-%m-%dT%H") + ':00:00Z'
end_date = systime.strftime("%Y-%m-%dT%H") + ':59:59Z'


# In[1059]:


appended_data = pd.DataFrame(columns=['STREET_ID', 'datetime'])


# In[1060]:


for i in snowice:
    try:
        rjson = requests.get("https://api.networkfleet.com/locations/vehicle/"+i+"/track?limit=60&with-start-date="+start_date+"&with-end-date="+end_date,
                       headers={'Authorization': "Bearer "+response['access_token'],
                                'Accept': "application/vnd.networkfleet.api-v1+json",
                                'Content-Type': "application/vnd.networkfleet.api-v1+json"}
                      ).json()

        if rjson['count'] != 0:
            x = pd.DataFrame(rjson)
            Name = pd.io.json.json_normalize(x['gpsMessage'])
            Nameedit = Name[['latitude', 'longitude', 'messageTime']]
            Nameedit['truck_name'] = i
            Nameedit['timeedit'] = pd.to_datetime(Nameedit['messageTime'])
            #Nameedit['hour'] = (Nameedit["timeedit"]-timezone).dt.hour
            Nameedit['datetime'] = (Nameedit['timeedit']-timezone).dt.strftime("%Y-%m-%d %H:00:00")
            geometry = [Point(xy) for xy in zip(Nameedit.longitude, Nameedit.latitude)]
            Nameedit1 = GeoDataFrame(Nameedit, geometry=geometry)
            Nameedit1 = Nameedit1.groupby(['truck_name', 'datetime'])['geometry'].apply(lambda x: LineString(x.tolist()))
            Nameedit1 = GeoDataFrame(Nameedit1, geometry='geometry')
            Nameedit1 = pd.DataFrame(Nameedit1.to_records())
            Nameedit1 = GeoDataFrame(Nameedit1, geometry='geometry')
            Nameedit1.crs = {'init' :'epsg:4326'}
            x1 = gpd.sjoin(Nameedit1, dataSrc, op='intersects')
            x1 = x1[['STREET_ID', 'datetime']]
            appended_data = appended_data.append(x1)
            print("success: "+ i)
        else:
            print("0 count: " +i)

    except:
        print ("fail: " + i)


# appended_data['datetime'] = appended_data['date'].astype(str) + " " + appended_data['hour'].astype(str) + ":00:00"

# In[1061]:


appended_data['datetime'] = pd.to_datetime(appended_data['datetime'])


# In[1062]:


res = appended_data.groupby('STREET_ID')['datetime'].max().reset_index()


# In[1063]:


mergeddata = dataSrc[['STREET', 'geometry', 'STREET_ID']].merge(res, left_on='STREET_ID', right_on='STREET_ID', how='right')


# In[1064]:


mergeddata_all = mergeddata


# In[1065]:


#mergeddata_all = pd.DataFrame(columns=['STREET', 'geometry', 'STREET_ID'])


# In[1066]:


#mergeddata_all = mergeddata_all.append(mergeddata)


# In[1067]:


#mergeddata_all = mergeddata_all.groupby(['STREET_ID'])['datetime'].max().reset_index()


# In[1068]:


#mergeddata_all = dataSrc[['STREET', 'geometry', 'STREET_ID']].merge(mergeddata_all, left_on='STREET_ID', right_on='STREET_ID', how='right')


# In[1069]:


mergeddata_all['datetime'] = mergeddata_all['datetime'].astype(str)
mergeddata['datetime'] = mergeddata['datetime'].astype(str)


# In[1070]:


with open('mergeddata.geojson', 'w') as f:
    f.write(mergeddata_all.to_json())



# In[1071]:


with open('last_hour.geojson', 'w') as f:
    f.write(mergeddata.to_json())


# In[1072]:


notplowed = dataSrc[(~dataSrc['STREET_ID'].isin(mergeddata_all['STREET_ID'].astype(object)))]


# In[1073]:


notplowed = notplowed[['STREET', 'geometry', 'STREET_ID']]


# In[1074]:


with open('notplowed.geojson', 'w') as f:
    f.write(notplowed.to_json())
