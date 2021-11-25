import json

path = "./data.json"

def format_json(path):
	with open(path, encoding="utf8") as jsonFile:
	    jsonObject = json.load(jsonFile)
	    jsonFile.close()
	return jsonObject

def get_trucks(jsonObject):
    return jsonObject['trucks']

def get_customers(jsonObject):
    return jsonObject['customers']

def get_home(jsonObject):
    return jsonObject['home']

if __name__ == '__main__':
    jsonObject = format_json(path)
    trucks = get_trucks(jsonObject)
    customers = get_customers(jsonObject)
    home = get_home(jsonObject)

    nb_vehicules = trucks['amount']