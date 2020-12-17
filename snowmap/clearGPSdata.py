import pandas as pd
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap')
gps_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
gps_data.to_csv('gps_data.csv', index = False)
