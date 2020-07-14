import numpy as np
import array
import random

import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

def read_tsp(filename):
    
    """
    Lee el fichero filename y devuleve la lista de coordenadas de cada ciudad
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        nodelist:: List, lista de coordenadas de cada nodo o ciudad
        N:: Int, número de nodos o ciudades
    """

    # Open input file
    infile = open(filename, 'r')

    # Read instance header
    Name = infile.readline().strip().split()[1] # NAME
    FileType = infile.readline().strip().split()[1] # TYPE
    Comment = infile.readline().strip().split()[1] # COMMENT
    Dimension = infile.readline().strip().split()[1] # DIMENSION
    EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
    infile.readline()

    # Read node list
    nodelist = []
    N = int(Dimension)
    for i in range(0, N):
        x,y = infile.readline().strip().split()[1:]
        nodelist.append([float(x), float(y)])

    # Close input file
    infile.close()
    
    return nodelist, N

def distance_matrix(nodelist, N):
    
    """
    Crea la matriz de distancias euclídeas entre ciudades a partir de la lista de coordenandas
    
    input:
        nodelist:: List, lista de coordenadas de cada nodo o ciudad
        N:: Int, número de nodos o ciudades
        
    output:
        distanceMatrix:: Array, matriz de distancias euclídeas
    """

    # Create the distance matrix
    distanceMatrix = np.zeros((N, N))
    for i in range(0, N):
        for j in range (0, N):
            if i != j:
                xDis = nodelist[i][0] - nodelist[j][0]
                yDis = nodelist[i][1] - nodelist[j][1]
                distanceMatrix[i][j] = round((np.sqrt((xDis ** 2) + (yDis ** 2))), 0)

    return distanceMatrix