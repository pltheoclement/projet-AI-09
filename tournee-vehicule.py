import json
import numpy as np

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

def get_areas(customers, nb_trucks, home):
    nb_areas = min(nb_trucks, len(customers))
    centers = []
    for n in range(nb_areas):
        centers.append(customers[n])

    #boucle à partir de là
    areas = [[] for i in range(nb_areas)]
    old_areas = None
    # On sépare l'espace actuel en nb_areas espaces
    while areas != old_areas:
        old_areas = areas.copy()
        areas = [[] for i in range(nb_areas)]
        for customer in customers:
            distances = [0 for i in range(nb_areas)]
            for i, center in enumerate(centers):
                distance = distance_between_customers(customer, center)
                distances[i] = distance
            index = get_index_of_min(distances)
            areas[index].append(customer)
            print(areas)
            print('\n')
        for n in range(nb_areas):
            center[n] = get_area_center(areas[n])
    return areas

def get_area_center(l):
    x = 0
    y = 0
    y_value_sum = 0
    x_value_sum = 0
    g_sum = 0
    for customer in l:
        x_value_sum += customer['x']*customer['value']
        y_value_sum += customer['y']*customer['value']
        g_sum += customer['value']

    x = x_value_sum / g_sum
    y = y_value_sum / g_sum
    return {'x' : x,'y' : y}

def distance_between_customers(c1, c2):
    c1_coord = np.array((c1['x'], c1['y']))
    c2_coord = np.array((c2['x'], c2['y']))
    d = np.linalg.norm(c1_coord-c2_coord)
    return d

def get_index_of_min(l):
    temp = min(l)
    return [i for i, j in enumerate(l) if j == temp][0]

def accessible_customers(customers, trucks):
    # éliminer les clients inaccessibles
    return 0

if __name__ == '__main__':
    jsonObject = format_json(path)
    trucks = get_trucks(jsonObject)
    # customers = accessible_customers(get_customers(jsonObject), trucks)
    customers = get_customers(jsonObject)
    home = get_home(jsonObject)

    nb_vehicules = trucks['amount']

    print(get_areas(customers, nb_vehicules, home))
