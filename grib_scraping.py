'''
This script scrapes data from Wikigrib and saves it in the file in JSON format.
It also can extract it from file and convert to dictionary.
Now only the second option is on.
'''

import requests
from bs4 import BeautifulSoup
import pprint
import json
import os

def get_html(url):
	'''
	Returns html of the page
	'''
	try:
		result = requests.get(url)
		result.raise_for_status()
		return result.text
	except requests.exceptions.HTTPError:
	    print ("Страница не найдена или превышен интервал ожидания " + url)
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
				grib_lat_name = grib_lat_name.replace(" ", "_")

				grib = {}
				grib[grib_lat_name] = {
					'rus_name': item.find('a', class_ = 'catcont-list__title').text,
					'link': item.find('a', class_ = 'catcont-list__title')['href'],
					'type': grib_type
				}

				print(grib[grib_lat_name]['rus_name'])

				grib[grib_lat_name]['description'], img_path = scrap_grib_detailed_data(grib[grib_lat_name]['link'], grib_lat_name)
			except:
				print('Страница, гриб ' + str(i) + ', ' + str(grib_num) + ' - возникла проблема с получением данных')
				continue

			if grib_lat_name not in mushrooms.keys():
				mushrooms.update(grib)
				grib_num += 1
			else:
				print(grib_lat_name + ' дублируется. Варианты: ' + mushrooms[grib_lat_name]['rus_name'] + ' (оставлен в нашем списке), ' + grib[grib_lat_name]['rus_name'] + ' (исключен)\n')
	

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

	print('Подождите немного, идет построение списка грибов... Это может занять несколько минут.\n')
	for section in sections:
		mushroom_dictionary.update(get_section_info(sections[section], section))

	return mushroom_dictionary


def save_dictionary_to_json_file(dict):
	json_dict = json.dumps(dict)

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


def scrap_grib_detailed_data(url, grib_name):
	'''
	Scraps detail info about the mushroom (description, pic) form mushroom page
	'''
	grib_info = {}

	try:
		html = get_html(url)
	except:
		"Не могу получить html детальной страницы"
		return False

	bs = BeautifulSoup(html, 'html.parser')
	div_with_description = bs.find("div", {"id": "entry"})

	img_path = ''

	for item in div_with_description.find_all('p'): 
		# if p  contains pic let's grab it
		if item.find('img'):
			# upload a pic into folder
			url = item.find('img')['src']
			try:
				response = requests.get(url)
				img_path = "main_pictures/" + grib_name + ".jpg"
			except:
				continue

			if response.status_code == 200:
				directory = 'main_pictures/'
				if not os.path.exists(directory):
				    os.makedirs(directory)
				with open(img_path, 'wb') as f:
					f.write(response.content)

		elif item.find('strong'):
			grib_param = item.find('strong').text.strip().strip(':')
			item.find('strong').extract()
			grib_text = item.text.strip('\n')
			grib_info[grib_param] = grib_text


	# returns grib description + if image is downloaded
	return grib_info, img_path


if __name__ == '__main__':

	#pprint.pprint(scrap_grib_detailed_data('http://wikigrib.ru/lisichka-obyknovennaya/', 'Gyroporus_cyanescens'))

	#For scraping mashrooms from WikiGrib
	# mushroom_dictionary = get_mushrooms_dictionary()
	# save_dictionary_to_json_file(mushroom_dictionary)
	#print_mushroom_dictionary(mushroom_dictionary)
	#pprint.pprint(mushroom_dictionary)

	# Print mushrooma from dictionary
	pprint.pprint(get_mushrooms_from_json_file())

	'''
	mushrooms = get_mushrooms_from_json_file()
	print_mushroom_dictionary(mushrooms)
	'''

	# TODO заменить пробелы на ниж подчеркивание
	#grib_d = get_section_info('http://wikigrib.ru/vidy/sedobnye-griby/', 'Съедобные')
	#print_mushroom_dictionary(grib_d)
	#pprint.pprint(grib_d)