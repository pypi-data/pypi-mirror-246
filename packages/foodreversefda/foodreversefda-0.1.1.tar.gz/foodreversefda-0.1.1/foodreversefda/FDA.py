import requests
import json

class food_reverse_info(object):
    def __init__(self, id):
        self.id = id

    def info(self):
        url = 'https://api.fda.gov/food/enforcement.json?search=event_id"{}"'.format(self.id)
        r = requests.get(url)
        outfile = open("food_reverse.json", "w")
        json.dump(r.json(), outfile, indent = 4)

