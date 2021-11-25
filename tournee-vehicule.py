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

def get_areas(customers, nb_trucks):
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
        for n in range(nb_areas):
            centers[n] = get_area_center(areas[n])
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
    center = dict()
    center['x'] = x
    center['y'] = y
    return center

def distance_between_customers(c1, c2):
    c1_coord = np.array((c1['x'], c1['y']))
    c2_coord = np.array((c2['x'], c2['y']))
    d = np.linalg.norm(c1_coord-c2_coord)
    return d

def get_index_of_min(l):
    temp = min(l)
    return [i for i, j in enumerate(l) if j == temp][0]

def remove_unaccessible_customers(customers, trucks, home):
    accessible_customers = []
    for customer in customers:
        if (2*distance_between_customers(home, customer) <= trucks['distance']):
            accessible_customers.append(customer)
    return accessible_customers

def coef_reduce_value(area, home):
    values = []
    distances = []
    for customer in area:
        values.append(customer['value'])
        distances.append(distance_between_customers(customer, home))

    
    min_value = max(values)
    min_distance = max(distances)
    print("\n")
    print(min_distance / min_value)
    print("\n")
    print("\n")
    return min_distance / min_value

def ppv(c, list_of_available_customers, coef):
    dist = 0
    choice = None
    for customer in list_of_available_customers:
        euclid_dist = distance_between_customers(c, customer)
        new_dist = (coef * customer['value']) / euclid_dist
        if new_dist > dist:
            dist = new_dist
            choice = customer
    return choice

def path_in_area(area, home, trucks):
    list_of_available_customers = area
    current_point = home
    fuel = trucks['distance']
    coef = coef_reduce_value(area, home)
    path = [current_point]
    total_value = 0
    while (fuel >= distance_between_customers(current_point, home)) and (len(list_of_available_customers) > 0):
        pot_next = ppv(current_point, area, coef)
        if fuel - (distance_between_customers(current_point, pot_next) + distance_between_customers(pot_next, home)) > 0 :
            fuel -= distance_between_customers(current_point, pot_next)
            current_point = pot_next
            total_value += current_point['value']
            list_of_available_customers.remove(current_point)
            path.append(current_point)
        else :
            list_of_available_customers.remove(pot_next)
    fuel -= distance_between_customers(current_point, home)
    path.append(home)
    return total_value, path

def main(customers, home, trucks):
    areas = get_areas(customers, trucks['amount'])
    total_value = 0
    all_paths = []
    for area in areas:
        [value, path] = path_in_area(area, home, trucks)
        total_value += value
        all_paths.append(path)
    return total_value, all_paths


if __name__ == '__main__':
    jsonObject = format_json(path)
    trucks = get_trucks(jsonObject)
    home = get_home(jsonObject)
    customers = remove_unaccessible_customers(get_customers(jsonObject), trucks, home)

    [total_value, all_paths] = main(customers, home, trucks)

    print(total_value)
    print('\n')

    print(all_paths)
