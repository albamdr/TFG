from read_knapsack_files import read_knapsack

def knapsack_greedy(filename):
    
    """
    Genera un individuo para el algoritmo genético a partir de la solución del algoritmo voraz
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
        
    output:
        individual:: Set, representante de la solución del algoritmo voraz
    """
    
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

    return individual  