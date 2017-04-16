import requests
from bs4 import BeautifulSoup
import pprint

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


def get_section_info(url):
	mushrooms = []

	i = 1
	while True:
		page_url = url + 'page/' + str(i) + '/'
		html = get_html(page_url)

		if not html:
			break

		bs = BeautifulSoup(html, 'html.parser')

		for item in bs.find_all('div', class_='catcont-list'):
			grib = {}
			grib['rus_name'] = item.find('a', class_ = 'catcont-list__title').text
			grib['lat_name'] = item.h4.span.text
			grib['link'] = item.find('a', class_ = 'catcont-list__title')['href']
			mushrooms.append(grib)

		i += 1	

	return mushrooms


if __name__ == '__main__':

	# Mushroom types for classification
	sections = {
		'Съедобные': 'http://wikigrib.ru/vidy/sedobnye-griby/',
		'Условно-съедобные': 'http://wikigrib.ru/vidy/uslovno-sedobnye/',
		'Несъедобные': 'http://wikigrib.ru/vidy/nesedobnye-griby/',
	}

	mushroom_dictionary = {
		'Съедобные': {},
		'Условно-съедобные': {},
		'Несъедобные': {},

	}

	print('Подождите немного, идет построение списка грибов... Это может занять около минуты.')
	for type in sections:
		mushroom_dictionary[type] = get_section_info(sections[type])

	pprint.pprint(mushroom_dictionary)