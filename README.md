# UCU_Map_project


## Description
This is the University project made by Bilusyak Dmytro
It inctludes the python module main.py, which generates the map and save it to Map.html
The Map will include the pointers on up to ten films which were filmed near the location inputed
Also it paints the country in red if it has more than 200 films, yellow if more than 10, green if less than 10, 
and if the country is painted grey - the database was unable to find this country.


P.S As you can see, there are also one_time_use module which makes city_coordinates.tsv 
and location_data files using the files that are in Origin_data folder, all of which where provided 
with the task, except worldcities.csv which was taken from https://simplemaps.com/data/world-cities

## Requirements 
```
pip install folium
```

## Usage
```bash
janusdg@xps:~/UCU/IT/Py/UCU/Labs/UCU_Map_project$ /usr/bin/python3 main.py
Вкажи рік 2004
Де ти? 4.200001, 69.00001

```
[]!(sample_of_execution)

## Output 
[]!(start_page)
This is what would you see if you run the module with these parameters

[]!(description)
If you move the map, you could see the names of the films

Also, keep in mind that there could happen a situation when all films were filmed at the same place, 
so that you wont be able to see all of them, until you zoom the map to it's maximum
[]!(all_in_one_place)



# The description of the html file
```
<!DOCTYPE html> - meaning that it should use the latest version of HTML5 

<head></head> - the header   

<body></body> - the main part of the page
<meta http-equiv="content-type" content="text/html; charset=UTF-8" /> - the desctiption of the html file and what it is for
<script></script> - the action to make
var - html varible
function - html function
<style> </style> - styling withot css
```
 
## Project status
The modules are ready to use and are up to date
