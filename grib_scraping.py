'''
This script scrapes data from Wikigrib and saves it in the file in JSON format.
It also can extract it from file and convert to dictionary.
Now only the second option is on.
'''

import requests
from bs4 import BeautifulSoup
import pprint
import json

def get_html(url):
	'''
	Returns html of the page
	'''
	try:
		result = requests.get(url)
		result.raise_for_status()
		return result.text
	except requests.exceptions.HTTPError:
	    # print ("Страница не найдена или превышен интервал ожидания " + url)
	    return False
	except requests.exceptions.RequestException:
		print ("Ошибка соединения со страницей " + url)
		return False


def get_section_info(url, type):
	mushrooms = []

	i = 1
	while True:
		page_url = url + 'page/' + str(i) + '/'
		html = get_html(page_url)

		if not html:
			break

		bs = BeautifulSoup(html, 'html.parser')

		for item in bs.find_all('div', class_='catcont-list'):
			grib_lat_name = item.h4.span.text
			grib = {}
			grib[grib_lat_name] = {
				'rus_name': item.find('a', class_ = 'catcont-list__title').text,
				'link': item.find('a', class_ = 'catcont-list__title')['href']
			}

			mushrooms.append(grib)

		i += 1	

	return mushrooms

def get_mushrooms_dictionary():
	# Mushroom types for classification
	sections = {
		'Съедобные': 'http://wikigrib.ru/vidy/sedobnye-griby/',
		'Условно-съедобные': 'http://wikigrib.ru/vidy/uslovno-sedobnye/',
		'Несъедобные': 'http://wikigrib.ru/vidy/nesedobnye-griby/',
	}

	mushroom_dictionary = []

	print('Подождите немного, идет построение списка грибов... Это может занять около минуты.')
	for type in sections:
		mushroom_dictionary.append(get_section_info(sections[type], type))

	#pprint.pprint(mushroom_dictionary)	
	return mushroom_dictionary


def save_dictionary_to_json_file(dict):
	json_dict = json.dumps(dict)
	# json.loads(json) - converts json to dictionary

	f = open('mushrooms.txt', 'w')
	f.write(json_dict) 
	f.close()

	#with open (“mushrooms.txt”, “w”) as file: 
	#	file.write(json) 


def get_mushrooms_from_json_file():
	f = open('mushrooms.txt', 'r')
	json_dict = f.read() 
	f.close()

	dictionary = json.loads(json_dict)
	return dictionary


if __name__ == '__main__':

	# mushroom_dictionary = get_mushrooms_dictionary()
	# save_dictionary_to_json_file(mushroom_dictionary)
	 pprint.pprint(get_mushrooms_from_json_file())
	# pprint.pprint(mushroom_dictionary)