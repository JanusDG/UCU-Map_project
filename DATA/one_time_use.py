def sort_all_years(path):
    """
    path to a file -> dict
    The finction returns the dict with years as a key, a value of 
    list, where the all films of this year are stored as a list with its 
    name as a 1st element and a list of it's location as 2nd element

    '1991': [['"101-kai me no puropozu"', ['Irima-cho, Chofu, Tokyo, Japan']], ... ]

    """
    def gen(path):
        for row in open(path).readlines():
            item = row.split("\t")
            if "(" not in item[0]:
                yield None
                continue
            name = item[0][:item[0].index("(") - 1]
            year = item[0][item[0].index("(") + 1 :item[0].index("(") + 5]
            item = item[1:]
            item = [i.strip() for i in item if i != '']

            yield name, year, item
    data = gen(path)

    dict_of_years = {}
    while True:
        try:
            item = next(data)
            if item == None:
                continue
            if item[1] not in dict_of_years.keys():
                dict_of_years[item[1]] = [[item[0],item[-1]]]
            else:
                dict_of_years[item[1]].append([item[0],item[-1]])
                
        except StopIteration:
            break

    temp = []
    for item in dict_of_years.keys():
        if not item.isdigit():
            temp.append(item)
    for item in temp:
        del dict_of_years[item]
    return dict_of_years


def save_changes(path, dict_to_write):
    """
    2006	"#1 Single"	['Los Angeles, California, USA']
    """
    with open(path, "w") as file:
        for key, value in dict_to_write.items():
            for element in value:
                file.write(f"{key}\t{element[0]}\t{element[1]}\n")


def repasse_file(path_read, path_write):
    with open(path_read, "r", encoding="utf-8") as read_file:
        for item in read_file.readlines():
            item = item.split(",")
            city = item[1].strip("\"")
            lat = item[2].strip("\"")
            lon = item[3].strip("\"")
            country = item[4].strip("\"")
            with open(path_write, "a") as read_file:
                read_file.write(country + "\t" + city + "\t" + lat + "\t" + lon + "\n")

    
def make_new_data():
    path_to_origin = "C:/Ucustud/ITshnik/Py/UCU/Labs/Labs2.index/Lab2.2/Lab2.2.2/DATA/locations.list"

    dict_to_write = sort_all_years(path_to_origin)

    path_to_rewrite = "C:/Ucustud/ITshnik/Py/UCU/Labs/Labs2.index/Lab2.2/Lab2.2.2/DATA/location_data.list"
    save_changes(path_to_rewrite, dict_to_write)
    
    path_read = "C:/Ucustud/ITshnik/Py/UCU/Labs/Labs2.index/Lab2.2/Lab2.2.2/DATA/worldcities.csv"
    path_write = "C:/Ucustud/ITshnik/Py/UCU/Labs/Labs2.index/Lab2.2/Lab2.2.2/DATA/city_coordinates.tsv"
    repasse_file(path_read, path_write)

if __name__ == "__main__":

    make_new_data()
