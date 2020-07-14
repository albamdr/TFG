def read_MIS(filename):
    
    """
    Lee el fichero filename y devuleve el númer de vértices, de aristas y el grafo
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        E:: Int, número de aristas
        V:: Int, número de vértiices
        G:: List, grafo en forma de lista de aristas G[i] es la lista de aristas que salen de i
    """
        
    # Open input file
    infile = open(filename, 'r')

    # Read instance header
    p, edge, V, E = infile.readline().strip().split()  # V: number of vertes, E: number of edges

    V = int(V)
    E = int(E)
    G = [[] for k in range(V)]

    for k in range(0,E):
        e, i, j = infile.readline().strip().split()
        G[int(i)-1].append((int(i),int(j)))
        
    return E, V, G
