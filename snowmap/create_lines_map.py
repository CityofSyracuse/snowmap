
# coding: utf-8

# In[401]:


import geopandas as gpd
from geopandas import GeoDataFrame
import pandas as pd
from shapely.geometry import shape, Point, mapping, LineString
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap')

# In[402]:


gdf_segments = gpd.read_file("streets.shp")


# In[403]:


gdf_segments.crs = {'init' :'epsg:2261'}
gdf_segments = gdf_segments.to_crs({'init': 'epsg:4326'})


# In[404]:


#shply_line = gdf_segments.geometry.unary_union


# In[432]:


gps_data = pd.read_csv("gps_data.csv")


# In[433]:


geometry = [Point(xy) for xy in zip(gps_data.longitude, gps_data.latitude)]
points_df = GeoDataFrame(gps_data, geometry=geometry)
#points_df['geometry'] = points_df.apply(lambda row: shply_line.interpolate(shply_line.project( row.geometry)), axis=1)


# In[435]:


lines = points_df.groupby(['truck_name', 'datetime']).filter(lambda x: len(x) > 1)


# In[436]:


lines = lines.groupby(['truck_name', 'datetime'])['geometry'].apply(lambda x: LineString(x.tolist()))


# In[437]:


lines_df = GeoDataFrame(lines, geometry='geometry')
lines_df = pd.DataFrame(lines_df.to_records())
lines_df = GeoDataFrame(lines_df, geometry='geometry')
lines_df.crs = {'init' :'epsg:4326'}


# In[426]:


#x1 = gpd.sjoin(lines_df, gdf_segments, op='intersects')
#x1 = x1[['STREET_ID', 'datetime']]


# In[427]:


#lines_df[lines_df.overlaps(gdf_segments)]


# In[428]:


#mergeddata = gdf_segments[['STREET', 'geometry', 'STREET_ID']].merge(x1, left_on='STREET_ID', right_on='STREET_ID', how='right')


# In[438]:


#mergeddata.to_file("mergeddata.shp")
#lines_df.to_file('/home/pi/snowmap/snowmap/lines_df.shp')
#points_df.to_file('/home/pi/snowmap/snowmap/points_df.shp')


# In[439]:


with open('lines_df.geojson', 'w') as f:
    f.write(lines_df.to_json())


# In[440]:


with open('points_df.geojson', 'w') as f:
    f.write(points_df.to_json())
