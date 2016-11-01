from bs4 import BeautifulSoup
from math import floor
from time import sleep
import requests
import googlemaps
import io
import json


def soupItUp(URL):
	content = requests.get(URL)
	soup = BeautifulSoup(content.text, "lxml")
	return soup

def losAngelesCities():
	URL = "https://en.wikipedia.org/wiki/List_of_cities_in_Los_Angeles_County,_California"
	soup = soupItUp(URL)

	cities = []
	for link in soup.find_all('a'):
	    title = link.text
	    if title:
	    	if "Cities within the County of Los Angeles" in title:
	    		break
	    	else:
	    		cities.append(title)

	cities = cities[5:-1]

	cities.remove("Industry")
	cities.remove("Avalon")

	return cities
	    	
def orangeCountyCities():
	URL = "http://ocgov.com/about/infooc/links/oc/occities"
	soup = soupItUp(URL)

	cities = []
	for link in soup.find_all('a'):
	    title = link.text
	    if title:
	    	if "City of" in title:
	    		city = " ".join(title.split()[2:])
	    		cities.append(city)

	return cities

def cityMatrix(origins):
	# google api 
	with io.open("google_secret.json") as cred:
		
		creds = json.load(cred)

	new_origins = []
	for origin in origins:
		origin = origin + ", California"
		new_origins.append(origin)

	#print(new_origins)
	destination = ["Costa Mesa, California"]


	gmaps = googlemaps.Client(**creds)

	matrix = gmaps.distance_matrix(new_origins, destination, units="imperial")
	city_names = [city.split(",")[0].replace(",", "") for city in matrix['origin_addresses']]
	distances = [float(row['elements'][0]['distance']['text'].split()[0]) for row in matrix['rows'] if row['elements'][0]['status'] == "OK"]
	dictionary = dict(zip(city_names, distances))


	return dictionary

def getDistances():
	LA = losAngelesCities()
	OC = orangeCountyCities()
	matrix_LA = cityMatrix(LA)
	sleep(20)
	matrix_OC = cityMatrix(OC)
	city_dictionary = {**matrix_LA, **matrix_OC}
	return city_dictionary

if __name__ == '__main__':

	getDistances()


