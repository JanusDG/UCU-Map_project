import folium


def create_year_dict(path_to_created_tsv, customer_year):
    """
    The function returns the dictionary with the 
    name of a film as its key and the info about it as the value
    """
    with open(path_to_created_tsv, "r",encoding='ISO-8859-1' ) as work_data:
        year_dict = {}
        
        for item in work_data.readlines():
            if item[:4] == str(customer_year):
                name = item.split("\t")[1].strip("\'\"\\")
                country_list_year = item[item.index('[') + 1 :item.index(']')].strip("'").split(", ")
                year_dict[name] = country_list_year

    return year_dict


def find_nearest(year_dict, dt, customer_latitude, customer_longitude):
    """
    The function returns the list of the films, which were 
    filmed near the specific location 
    """
    all_cities = []
    i = 0.5
    while True:
        for key, value in year_dict.items():
            for point in value:
                
                if point in dt.keys():
                    city_latitude = float(dt[point][0])
                    city_longitude = float(dt[point][1])
                    if abs(customer_latitude - city_latitude) < i and abs(customer_longitude - city_longitude) < i:
                        all_cities.append([key, point, city_latitude, city_longitude])
                        if len(all_cities) > 10 :
                            return all_cities
                        
        i += 0.5


def deferentiate(year_dict):

    """
    The function returns the dictioanry with the country as the key 
    and the number of films, which were filmed in that year

    {country: number of appearings in films}
    """
    nanana = {}
    for value in year_dict.values():
        for country in value:
            if country not in nanana.keys():
                nanana[country] = 1
            else:
                nanana[country] += 1

    return nanana
                

def create_needed_dictionary(path_to_file):
    """
    The function returns the dictionary with the 
    name of a film as its key and the list of its coordinates as the value
    using the tsv file and the customer's year 
    """

    with open(path_to_file, "r", encoding="utf-8") as file:
        real_coordinates = file.readlines()
        dt = {}
        for item in real_coordinates[1:]:
            item = item.split("\t")
            # for i in item:
            if ("." not in item[2] or "." not in item[3]) and (not item[2].isdigit() or not item[3].isdigit()):
                continue
            temp = [item[2],item[3].strip()]
            dt[item[1]] = [float(item) for item in temp]
    # print(dt)
    return dt

           
def create(list_of_nearest):
    """
    the function splits the info about the nearest films
    """
    lat = []
    lon = []
    text = []

    def isunique(item, lst):
        return item in lst

    for item in list_of_nearest:
        while isunique([item[-2], item[-1]], [[temp[-2], temp[-1]] for temp in list_of_nearest if temp != item]):
            item[-2] = str(float(item[-2]) + 0.00008)
            item[-1] = str(float(item[-1]) + 0.00008)


    for item in list_of_nearest:
        lat.append(item[-2])
        lon.append(item[-1])
        text.append(item[0])

    return lat, lon, text


def build_marks(lat, lon, text, data_storage, location):
    """
    The function creates the html file with the map with needed 
    pointers on the films and the colors for each country, depending 
    on the number of films, which were filmed there
    """
    lat, lon, text = create(list_of_nearest)

    map = folium.Map(location=location, zoom_start=7)

    nearest_films = folium.FeatureGroup(name="Nearby filmography")

    for lat, lon, text in zip(lat, lon, text):
        nearest_films.add_child(folium.CircleMarker(location=[lat, lon],
                                            radius=10,
                                            popup="Film name: "+text,
                                            fill_color="yellow",
                                            color='red',
                                            fill_opacity=0.5))

    map.add_child(nearest_films)


    area = folium.FeatureGroup(name="Number of fims in your year")

    area.add_child(folium.GeoJson(data=open('DATA/Origin_data/world.json', 'r',
                             encoding='utf-8-sig').read(),
                                style_function=lambda x: {'fillColor':'grey' if x['properties']['NAME'] not in data_storage.keys()
                        else "green" if data_storage[x['properties']['NAME']] < 10 
                        else 'yellow' if 10 <= data_storage[x['properties']['NAME']] < 200
                        else "red"  ,"color":"black","weight": 1})) 

    # map.add_child(fg_hc)
    map.add_child(area)

    map.add_child(folium.LayerControl())
    map.save('Map.html')


def create_covering(data_storage, dt):
    """
    This function make the proper dictionary to 
    make build_marks function able to work with .json file 
    """
    result = {}

    for key, value in dt.items():
        if key in data_storage.keys():
            result[str(value)] = data_storage[key]
        else:
            continue
    return result


def normal_input():
    """
    The function make the customer unable to input wrong coordinates
    """
    while True:
        try:
            customer_year = int(input("Вкажи рік "))
            if customer_year in range(1900, 2021):
                break
        except IndexError:
            continue
        except ValueError:
            continue

    while True:
        try:
            customer_location = [float(item) for item in (input("Де ти? ").split(","))]
            if abs(customer_location[0]) <= 90 and abs(customer_location[1]) <= 90:
                break
        except IndexError:
            continue
        except ValueError:
            continue
         
    return customer_year, customer_location


if __name__ == "__main__":

    answer = normal_input()
    customer_year = answer[0]
    customer_location = answer[1]
    customer_latitude = customer_location[0]
    customer_longitude = customer_location[1]
    

    year_dict = create_year_dict(r"DATA/location_data.list", customer_year)
    data_storage = deferentiate(year_dict)
    dt = create_needed_dictionary(r"DATA/city_coordinates.tsv")
    list_of_nearest = find_nearest(year_dict, dt, customer_latitude, customer_longitude)

    dict_to_build_covering = create_covering(data_storage, dt)

    lat, lon, text = create(list_of_nearest)
    build_marks(lat, lon, text, data_storage, customer_location)

    deferentiate(year_dict)
    