def read_knapsack(filename):
    
    """
    Lee el fichero filename y devuleve el número de items, el peso máximo de la mochila y los items
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        N:: Int, número de items
        max_weight:: Int, peso máximo de la mochila
        items:: Set, conjunto de tuplas (valor,peso) que representan los items        
    """
    
    # Open input file
    infile = open(filename, 'r')

    # Read instance header
    N, MAX_WEIGHT = infile.readline().strip().split()  # Number of items, maximum weight
    max_weight = int(MAX_WEIGHT)
    
    items = {}
    N = int(N)
    for i in range(0, N):
        value, weight = infile.readline().strip().split()
        items[i] = (float(value), float(weight))

    return N, max_weight, items