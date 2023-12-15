import requests
import json

class Classification(object):
    def __init__(self, class_type, limit):
        if class_type == 1:
            self.classification = "Class+I"
        elif class_type == 2:
            self.classification = "Class+II"
        elif class_type == 3:
            self.classification = "Class+III"
        else:
            raise ValueError("Error: no match found (classification level 1~3)")
        
        self.limit = limit

    def class_get(self):
        url = f'https://api.fda.gov/food/enforcement.json?search=classification:{self.classification}&limit={self.limit}'
        response = requests.get(url)
        
        if response.ok:
            with open("food_reverse_class.json", "w") as outfile:
                json.dump(response.json(), outfile, indent = 4)
        else:
            print(f"Error: {response.status_code} - {response.text}")
