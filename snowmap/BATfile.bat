conda activate exe

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\clearGPSdata.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\vehicleList.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\Snowplow_mapping_geojson_getting_started.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\Snowplow_mapping_geojson.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\pullGPSdata.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\odometer_readings.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\create_polygons.py"

python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\create_lines_map.py"

#!/bin/bash
cd Desktop/City of Syracuse/snowmap-master/snowmap/snowmap
git add *

git commit -m "Update the map"


git push https://samedelstein:Syr2021!@github.com/CityOfSyracuse/snowmap.git --all

EXIT/B