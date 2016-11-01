from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from getCities import losAngelesCities, orangeCountyCities, getDistances
import io
import json
import pyexcel



def runProgram():
	distances = {'South Gate': 37.0, 'Commerce': 35.6, 'Monrovia': 49.3, 'Maywood': 39.0, 'Hawthorne': 39.7, 'Cudahy': 37.5, 'Calabasas': 70.2, 'South El Monte': 39.6, 'Baldwin Park': 43.4, 'San Dimas': 38.3, 'Pomona': 36.9, 'Bell Gardens': 32.5, 'Sierra Madre': 52.7, 'Lake Forest': 16.2, 'Santa Fe Springs': 30.5, 'Lakewood': 25.3, 'Diamond Bar': 31.6, 'Duarte': 47.0, 'Glendora': 42.5, 'Seal Beach': 20.0, 'Lomita': 37.8, 'Huntington Beach': 6.1, 'Los Alamitos': 19.0, 'San Clemente': 29.9, 'Covina': 40.2, 'El Segundo': 42.5, 'Laguna Hills': 18.3, 'Pasadena': 50.4, 'Placentia': 19.8, 'Hermosa Beach': 38.3, 'Paramount': 29.0, 'Montebello': 37.1, 'Manhattan Beach': 39.2, 'La Habra Heights': 33.3, 'West Covina': 42.3, 'Costa Mesa': 1.0, 'Cypress': 18.5, 'Alhambra': 43.8, 'Azusa': 44.1, 'West Hollywood': 53.4, 'Downey': 30.0, 'South Pasadena': 48.3, 'Rancho Palos Verdes': 42.4, 'Artesia': 24.8, 'Compton': 32.1, 'Long Beach': 29.9, 'Bell': 37.6, 'San Juan Capistrano': 23.0, 'La Habra': 26.8, 'Agoura Hills': 76.1, 'La Palma': 25.3, 'Bellflower': 26.7, 'Rolling Hills': 42.1, 'Cerritos': 25.4, 'Gardena': 34.3, 'Rancho Santa Margarita': 26.5, 'Rolling Hills Estates': 41.2, 'Laguna Niguel': 21.2, 'Claremont': 40.4, 'Monterey Park': 43.1, 'Burbank': 52.0, 'Torrance': 36.3, 'Laguna Beach': 17.3, 'Santa Ana': 10.9, 'Arcadia': 50.7, 'Walnut': 33.4, 'Vernon': 41.3, 'Dana Point': 26.7, 'La Mirada': 27.3, 'Norwalk': 28.0, 'La Puente': 37.4, 'Laguna Woods': 15.7, 'Brea': 23.0, 'Pico Rivera': 32.8, 'Malibu': 68.7, 'San Fernando': 63.5, 'Culver City': 46.7, 'Glendale': 48.0, 'Palmdale': 107.0, 'Fountain Valley': 8.2, 'Mission Viejo': 17.9, 'La Cañada Flintridge': 53.9, 'Tustin': 9.9, 'Fullerton': 23.0, 'Bradbury': 47.1, 'Buena Park': 21.9, 'Stanton': 15.5, 'Palos Verdes Estates': 43.8, 'Carson': 29.9, 'Aliso Viejo': 16.8, 'Westlake Village': 78.0, 'Newport Beach': 1.9, 'Rosemead': 42.2, 'Irvine': 9.8, 'Temple City': 45.8, 'Garden Grove': 18.3, 'Redondo Beach': 37.3, 'San Gabriel': 45.4, 'Villa Park': 14.9, 'Santa Monica': 51.2, 'Orange': 13.2, 'Hawaiian Gardens': 22.3, 'Inglewood': 42.3, 'Lynwood': 34.0, 'Hidden Hills': 71.2, 'Huntington Park': 39.8, 'Beverly Hills': 53.2, 'Anaheim': 17.1, 'Los Angeles': 41.8, 'Irwindale': 46.3, 'Westminster': 12.3, 'El Monte': 41.6, 'Lawndale': 36.2, 'Santa Clarita': 76.8, 'Whittier': 31.4, 'Signal Hill': 23.9, 'San Marino': 47.1, 'La Verne': 37.9, 'Lancaster': 114.0, 'Yorba Linda': 21.3}
	terms = ['Indian Restaurant']
	with io.open('config_secret.json') as cred:
	    creds = json.load(cred)
	    auth = Oauth1Authenticator(**creds)
	    client = Client(auth)
	    findBusinesses(client, losAngelesCities(), terms, distances, "LA_v2")
	    findBusinesses(client, orangeCountyCities(), terms, distances, "OC_v2")


    
def findBusinesses(client, cities, terms, distances, county = "Los Angeles"):
	records = []
	is_artesia = False
	header = ['Name', 'Category', 'Phone Number', 'Yelp URL', 'Street Address', 'City', 'Distance', 'Yelp Rating', 'Review Count', 'Contacted?']
	records.append(header)
	for city in cities:
		print(city)
		city_distance = distances[city]
		if city == "Artesia":
			is_artesia = True
			terms.append('Indian Clothing Store')
		for term in terms:
			print(term)
			params = { 'term': term }
			response = client.search(city + ', California', **params)

			for business in response.businesses:
				if business.location.city == city:
					row = []
					row.extend((business.name, term, business.display_phone, business.url, str(business.location.address), business.location.city, str(city_distance), str(business.rating), str(business.review_count), "No"))
					records.append(row)
		if is_artesia:
			terms.remove('Indian Clothing Store')
			is_artesia = False
	pyexcel.save_as(array=records, dest_file_name=county + ".xls")

# excel sheet schema
# Name, Phone #, Website, Street Address, City, Contacted, Status

if __name__ == '__main__':

	runProgram()

