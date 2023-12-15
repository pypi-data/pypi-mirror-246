import requests
import json

class ID(object):
    def __init__(self, ids):
        self.ids = ids

    def id_get(self):
        all_data = {}
        for event_id in self.ids:
            url = f'https://api.fda.gov/food/enforcement.json?search=event_id:"{event_id}"'
            response = requests.get(url)

            if response.ok:
                all_data[event_id] = response.json()
            else:
                all_data[event_id] = "Error: " + response.text

        with open("food_reverse_id.json", "w") as outfile:
            json.dump(all_data, outfile, indent = 4) 

