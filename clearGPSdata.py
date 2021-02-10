import pandas as pd
import os
os.chdir("C:/Users/adarcangelo/Downloads/snowmap-master/snowmap-master/snowmap")
gps_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
gps_data.to_csv('gps_data.csv', index = False)
