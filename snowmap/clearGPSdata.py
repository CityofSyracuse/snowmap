import pandas as pd
gps_data = pd.DataFrame(columns=['latitude','longitude','messageTime','odometer.value','truck_name','timeedit','datetime'])
gps_data.to_csv('/home/pi/snowmap/snowmap/gps_data.csv', index = False)
