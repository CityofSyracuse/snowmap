@echo on
call C:\Users\adarcangelo\anaconda3\Scripts\activate.bat

call conda activate exe

call python "C:\Users\adarcangelo\Desktop\snowmap-master\snowmap\clearGPSdata.py"

call python "C:\Users\adarcangelo\Desktop\snowmap-master\snowmap\pullGPSdata.py"

call python "C:\Users\adarcangelo\Desktop\snowmap-master\snowmap\create_polygons.py"

#!/bin/bash
call cd C:\Users\adarcangelo\Desktop\snowmap-master\snowmap\
call git add *

call git commit -m "Update the map"

call git push https://adarcang@github.com/CityofSyracuse/snowmap.git --all
