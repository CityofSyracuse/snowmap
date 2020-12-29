@echo on
call C:\Users\adarc\anaconda3\Scripts\activate.bat

call conda activate exe

call python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\clearGPSdata.py"

call python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\pullGPSdata.py"

call python "C:\Users\adarc\Desktop\City of Syracuse\snowmap-master\snowmap\snowmap\snowmap\create_polygons.py"

#!/bin/bash
call cd Desktop/City of Syracuse/snowmap-master/snowmap/snowmap
call git add *

call git commit -m "Update the map"

call git push https://adarcang:Syr2021!@github.com/CityofSyracuse/snowmap/tree/master/snowmap.git --all
