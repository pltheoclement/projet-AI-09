import json
import random

# chaque point peut être placé sur une grille de 20x20 allant de 0 à 20 en x et en y
# Chaque instance contient un seul dépot appelé home
# Chaque instance peut contenir de 1 à 100 clients appelés customers
# Chaque instance peut contenir de 1 à 20 véhicules appelés trucks
# Les camions de chaque instance peuvent parcourir une distance de 10 à 90
# Chaque client à une valeur pouvant aller de 5 à 300

GRID = 400
MIN_CUSTOMERS = 10000
MAX_CUSTOMERS = 10001
MIN_TRUCKS = 100
MAX_TRUCKS = 101
MIN_VALUE = 5
MAX_VALUE = 500
MIN_DISTANCE = 800
MAX_DISTANCE = 801
MAX_SEED = 999999999

def get_random_home(grille):
    home = {
        "x": random.randint(0, grille),
        "y": random.randint(0, grille)
    }
    return home

def get_random_trucks(min_trucks, max_trucks, min_distance, max_distance):
    trucks = {
        "amount": min_trucks,
        "distance": min_distance
    }
    return trucks

def get_random_customers(grille, home, min_customers, max_customers, min_value, max_value):
    nb_customers = min_customers
    customers = []
    unavailble_places = [(home["x"], home["y"])]
    while len(customers) < nb_customers:
        attemp = (random.randint(0, grille), random.randint(0, grille))
        if attemp not in unavailble_places:
            unavailble_places.append(attemp)
            customers.append({
                "x": attemp[0],
                "y": attemp[1],
                "value": random.randint(min_value, max_value)
            })
        print(len(customers))
    return customers

def create_instance(number, grille, min_customers, max_customers, min_value, max_value, min_trucks, max_trucks, min_distance, max_distance):
    random.seed(number)
    home = get_random_home(grille)
    trucks = get_random_trucks(min_trucks, max_trucks, min_distance, max_distance)
    customers = get_random_customers(grille, home, min_customers, max_customers, min_value, max_value)

    instance = {
        "home": home,
        "trucks": trucks,
        "customers": customers
    }
    return instance

def create_multiple_instances(nb_instances):
    instances = {}
    for i in range(nb_instances):
        instances[i] = create_instance(i, GRID, MIN_CUSTOMERS, MAX_CUSTOMERS, MIN_VALUE, MAX_VALUE, MIN_TRUCKS, MAX_TRUCKS, MIN_DISTANCE, MAX_DISTANCE)
    return instances

if __name__ == "__main__":
    instances = create_multiple_instances(1)
    jsonObject = json.dumps(instances)
    jsonFile = open("dataAntiSolver.json", "w")
    jsonFile.write(jsonObject)
    jsonFile.close()