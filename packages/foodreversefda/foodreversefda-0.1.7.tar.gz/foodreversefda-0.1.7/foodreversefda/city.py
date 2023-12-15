import requests
import json

class City(object):
    def __init__(self, cities, limit):
        self.cities = cities
        self.limit = limit

    def city_get(self):
        all_data = {}
        for city in self.cities:
            url = f'https://api.fda.gov/food/enforcement.json?search=city:{city}&limit={self.limit}'
            response = requests.get(url)
        
            if response.ok:
                all_data[city] = response.json()
            else:
                all_data[city] = "Error: " + response.text

        with open("food_reverse_city.json", "w") as outfile:
            json.dump(all_data, outfile, indent = 4)
