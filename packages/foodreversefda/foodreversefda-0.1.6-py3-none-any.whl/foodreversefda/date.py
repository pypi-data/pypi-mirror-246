import requests
import json

class Date(object):
    def __init__(self, start, end, limit):
        self.start = start
        self.end = end 
        self.limit = limit 

    def date_get(self):
        url = f'https://api.fda.gov/food/enforcement.json?search=report_date:[{self.start}+TO+{self.end}]&limit={self.limit}'
        response = requests.get(url)
        
        if response.ok:
            with open("food_reverse_date.json", "w") as outfile:
                json.dump(response.json(), outfile, indent = 4)
        else:
            print(f"Error: {response.status_code} - {response.text}")
