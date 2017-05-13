import json
import os

def get_mushrooms_from_json_file():
	f = open('mushrooms.txt', 'r')
	json_dict = f.read() 
	f.close()

	dictionary = json.loads(json_dict)
	return dictionary

def get_simple_mushroom_name(name):
	name_list = name.split()
	return name_list[0]

def get_grib_info_by_eng_name (eng_name):
	name_matching = {
	    'champignon': "Agaricus_bernardii", # шампиньон
	    'chanterelle': "Cantharellus_cibarius", # лисичка
        'amanita': "Amanita_muscaria",  # мухомор
		'porcini': "Boletus_betulicola"  # белый
    }

	mushrooms = get_mushrooms_from_json_file()

	lat_name = name_matching.get(eng_name, '')

	mushrooms[lat_name]['rus_name_simple'] = get_simple_mushroom_name(mushrooms[lat_name][rus_name])

	return mushrooms[lat_name]


if __name__ == "__main__":
	name = 'champignon'
	grib = get_grib_info_by_eng_name(name)
	print(grib)
	print(get_simple_mushroom_name(grib['rus_name']))