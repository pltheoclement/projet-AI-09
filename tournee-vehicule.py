import json
import numpy as np
import matplotlib.pyplot as plt
import random


path = "./data.json"

# Fonction permettant de récupérer les données depuis un fichier JSON
def format_json(path):
	with open(path, encoding="utf8") as jsonFile:
	    jsonObject = json.load(jsonFile)
	    jsonFile.close()
	return jsonObject

# Fonction permettant de récupérer les données liées au camions à partir de l'objet JSON
def get_trucks(jsonObject):
    return jsonObject['trucks']

# Fonction permettant de récupérer les données liées au clients à partir de l'objet JSON
def get_customers(jsonObject):
    return jsonObject['customers']

# Fonction permettant de récupérer les données liées au dépot à partir de l'objet JSON
def get_home(jsonObject):
    return jsonObject['home']

# Cette fonction permet de découper le nuage de point en plusieurs aires.
# Params : 
#   customers : une liste de points avec des valeurs
#   nb_trucks : le nombre de camions disponible pour la tournée
#
# Return : Une liste de liste de points.
# Catte fonction découpe l'espace en plusieurs zone. Le nombre de zones est déterminé par le nombre de camions.
# Chaque camion fera une tournée dans une et une seule zone
def get_areas(customers, nb_trucks):
    # Dans le cas où il y a plus de camions que de clients, chaque zone représentera un seul client.
    nb_areas = min(nb_trucks, len(customers))
    centers = []

    # On choisi un client par zone pour débuter notre découpage
    for n in range(nb_areas):
        centers.append(customers[n])

    areas = [[] for i in range(nb_areas)]
    old_areas = None
    # On sépare l'espace actuel en nb_areas espaces
    # tant que le découpage en zone n'évolue pas d'une instance à l'autre on continue.
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
        
        # On calcule les centres de gravité des différentes zones calculées. Ces centres servent à trouver les points les plus proches.
        for n in range(nb_areas):
            centers[n] = get_area_center(areas[n])
    return areas

# FOnction servant à calculer le centre de gravité d'un nuage de point
# On lui fournie une liste de points, elle en ressort son centre de gravité
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

# Fonction permettant de calculer la distance euclidienne entre deux points
def distance_between_customers(c1, c2):
    c1_coord = np.array((c1['x'], c1['y']))
    c2_coord = np.array((c2['x'], c2['y']))
    d = np.linalg.norm(c1_coord-c2_coord)
    return d

# FOnction permettant de retourner le premier index de la plus petite valeur d'une liste.
def get_index_of_min(l):
    temp = min(l)
    return [i for i, j in enumerate(l) if j == temp][0]

# Certains clients ne sont pas acessibles par les camions, on les retire donc de notre domaine d'étude.
def remove_unaccessible_customers(customers, trucks, home):
    accessible_customers = []
    for customer in customers:
        if (2*distance_between_customers(home, customer) <= trucks['distance']):
            accessible_customers.append(customer)
    return accessible_customers

# Cette fonction implémente l'algorithme du plus proche voisin.
# On cherche ici à maximiser la distance. La distance n'est pas la distance euclidienne mais la valeur atténuée par le coef divisé par la distance euclidienne 
def ppv(c, list_of_available_customers):
    dist = 0
    choice = None
    for customer in list_of_available_customers:
        euclid_dist = distance_between_customers(c, customer)
        new_dist = (customer['value']) / euclid_dist
        if new_dist > dist:
            dist = new_dist
            choice = customer
    return choice

# Cette fonction calcul le chemin d'un camion au sein d'un espace de recherche
def path_in_area(area, home, trucks):
    list_of_available_customers = area
    current_point = home
    fuel = trucks['distance']
    path = [current_point]
    total_value = 0
    while (fuel >= distance_between_customers(current_point, home)) and (len(list_of_available_customers) > 0):
        pot_next = ppv(current_point, area)
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

# cette fonction fait boucler la précédente sur tous les espaces précédents et en retourne la valeur totale obtenue ainsi que l'ordre de visite des clients dans les différentes tournées.
def main(customers, home, trucks):
    areas = get_areas(customers, trucks['amount'])
    total_value = 0
    all_paths = []
    for area in areas:
        [value, path] = path_in_area(area, home, trucks)
        total_value += value
        all_paths.append(path)
    return total_value, all_paths


# Fonctionsservant à l'affichage des points
def display_points(li, home):
    x = np.array([])
    y = np.array([])
    for element in li:
        x = np.append(x, element['x'])
        y = np.append(y, element['y'])
    plt.scatter(x, y,color="black")
    plt.scatter(home['x'], home['y'],color="red")

def display_path(all_path):
    for path in all_path:
        col = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0]
        for i, element in enumerate(path[:-1]):
            x = [element['x'], path[i+1]['x']]
            y = [element['y'], path[i+1]['y']]
            plt.plot(x, y, color=col) 

if __name__ == '__main__':
    jsonObject = format_json(path)
    trucks = get_trucks(jsonObject)
    home = get_home(jsonObject)
    customers = get_customers(jsonObject)
    available_customer = remove_unaccessible_customers(customers, trucks, home)
    display_points(customers, home)

    [total_value, all_paths] = main(available_customer, home, trucks)

    print("La valeur totale obtenue par les différentes tourneés est : {}".format(total_value))
    print('\n')
    for i,path in enumerate(all_paths):
        print("la tournée du camion {} est : {}".format(i, path))
    display_points(customers, home)
    display_path(all_paths)
    plt.show()
