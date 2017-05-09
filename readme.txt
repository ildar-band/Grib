==========================================
Description how all these scripts work
==========================================

1) grib_scraping.py - it scrapes all the data about mushrooms from Wikigrib site and writes it into file "mushrooms.txt". Then you can just take it back from the file using the func "get_mushrooms_from_json_file" (it will be returned in the dictionary format, where the keys are the latin mushrooms names). If you want to get also grib images from Wikigrib you should run "get_mushrooms_dictionary()"

2) image_scraper.py - scrapes a bunch of images from different search engines. It's under construction at the moment (can scrape by only one keyword)