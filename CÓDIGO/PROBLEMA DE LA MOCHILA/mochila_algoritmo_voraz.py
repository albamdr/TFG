from read_knapsack_files import read_knapsack
import time

def knapsack_greedy(filename):
    
    """
    Algoritmo voraz para resolver instancias del problema de la mochila
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
        
    output:
        knapsack:: List, lista de items incluidos en la mochila
        knapsack_value:: Int o Float (dependiendo de la instancia) 
        end-start:: Float, tiempo que tarda el algoritmo voraz en llegar a la solución, expresado en segundos
    """
    start = time.time()
    
    N, MAX_WEIGHT, items = read_knapsack(filename)

    # sort de items by their density (value/weight)
    density_items = []
    for i in range(len(items)):
        density = items[i][0] / items[i][1]
        density_items.append(((items[i], i), density))

    density_items.sort(reverse=True, key=lambda x: x[1])
    knapsack_weight = 0
    knapsack_value = 0
    knapsack = []
    for i in range(len(density_items)):
        (value, weight), j = density_items[i][0]
        if knapsack_weight + weight <= MAX_WEIGHT:
            knapsack_weight += weight
            knapsack_value += value
            knapsack.append(j)
    
    individual = set(knapsack)
    
    end = time.time()

    return knapsack, knapsack_value, end-start