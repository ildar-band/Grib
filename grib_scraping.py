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


def get_section_info(url, grib_type):
	'''
	Gets information for one of the sections (eatable etc)
	'''
	mushrooms = {}

	i = 1
	while True:
		page_url = url + 'page/' + str(i) + '/'
		#print(page_url)
		html = get_html(page_url)

		if not html:
			break

		bs = BeautifulSoup(html, 'html.parser')

		grib_num = 0

		for item in bs.select("section.post.type-post"): 

			if not item:
				print('Элемент <section> не найден на странице')
				continue

			try:
				grib_lat_name = item.h4.span.text
				grib = {}
				grib[grib_lat_name] = {
					'rus_name': item.find('a', class_ = 'catcont-list__title').text,
					'link': item.find('a', class_ = 'catcont-list__title')['href'],
					'type': grib_type
				}
			except:
				print(item.prettify())
				continue

			if grib_lat_name not in mushrooms.keys():
				mushrooms.update(grib)
				grib_num += 1
			else:
				print(grib_lat_name + ' дублируется. Варианты: ' + mushrooms[grib_lat_name]['rus_name'] + ' (оставлен в нашем списке), ' + grib[grib_lat_name]['rus_name'] + ' (исключен)\n')
	

			#pprint.pprint(mushrooms)


		# print('Количество грибов на странице ' + str(i) + ': ' + str(grib_num))
		# print(len(mushrooms))

		i += 1	

	return mushrooms

def get_mushrooms_dictionary():
	# Mushroom types for classification
	sections = {
		'Съедобные': 'http://wikigrib.ru/vidy/sedobnye-griby/',
		'Условно-съедобные': 'http://wikigrib.ru/vidy/uslovno-sedobnye/',
		'Несъедобные': 'http://wikigrib.ru/vidy/nesedobnye-griby/',
	}

	mushroom_dictionary = {}

	print('Подождите немного, идет построение списка грибов... Это может занять около минуты.\n')
	for section in sections:
		mushroom_dictionary.update(get_section_info(sections[section], section))
		# print(type(get_section_info(sections[section], section)))

	#pprint.pprint(mushroom_dictionary)	
	# print('общее количество грибов: ' + str(count(mushroom_dictionary)))
	return mushroom_dictionary


def save_dictionary_to_json_file(dict):
	json_dict = json.dumps(dict)
	# json.loads(json) - converts json to dictionary

	f = open('mushrooms.txt', 'w')
	f.write(json_dict) 
	f.close()


def get_mushrooms_from_json_file():
	f = open('mushrooms.txt', 'r')
	json_dict = f.read() 
	f.close()

	dictionary = json.loads(json_dict)
	return dictionary

def print_mushroom_dictionary(dict):
	i = 1
	for m in dict:
		print(i)
		pprint.pprint(m)
		pprint.pprint(dict[m])
		i += 1


if __name__ == '__main__':

	#For scraping mashrooms from WikiGrib
	mushroom_dictionary = get_mushrooms_dictionary()
	save_dictionary_to_json_file(mushroom_dictionary)
	print_mushroom_dictionary(mushroom_dictionary)

	# Print mushrooma from dictionary
	# pprint.pprint(get_mushrooms_from_json_file())

	'''
	mushrooms = get_mushrooms_from_json_file()
	print_mushroom_dictionary(mushrooms)
	'''

	# TODO заменить пробелы на ниж подчеркивание
	#grib_d = get_section_info('http://wikigrib.ru/vidy/sedobnye-griby/', 'Съедобные')
	#print_mushroom_dictionary(grib_d)
	#pprint.pprint(grib_d)