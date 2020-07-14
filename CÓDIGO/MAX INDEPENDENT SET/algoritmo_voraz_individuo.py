

from read_MIS_files import read_MIS

import time

def sort_vertex_by_degree(G, N): #G=graph N=number of vertex
    
    """
    Ordena los vértices por grado, de menor a mayor
    
    input:
        G:: List, grafo en forma de lista de aristas
        N:: Int, número de vértices
        
    output:
        grades:: List, lista de vértices ordenados por grado, de menor a mayor
    """
    
    grades = [0 for i in range(N)] #lista de grados grades[i] es el grado del vértice i
    for edges_list in G:
        for edge in edges_list:
            i,j = edge
            grades[i-1] +=1
            grades[j-1] +=1
    grades = [(i+1,grades[i]) for i in range(N)] #lista de la forma (vertice,grado)
    grades.sort(reverse=False, key=lambda x: x[1]) #ordenamos la lista por grado de menor a mayor
    grades = [i[0] for i in grades] #nos quedamos con los vértices ordenados
    return grades #lista de vértices ordenados por grado de menor a mayor
    
def neighbours(G, N): #generamos una lista de listas de vecinos de cada vértice
    neighbours = [set() for i in range(N)] #neighbours[i] set de vecinos del vértice i+1
    for edges_list in G:
        for edge in edges_list:
            i,j = edge
            neighbours[i-1].add(j)
            neighbours[j-1].add(i)
    return neighbours
    
def greedy_mvc(filename):
    
    """
    Genera un individuo para el algoritmo genético a partir de la solución del algoritmo voraz
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        list_mis:: List, representante de la solución del algoritmo voraz
    """
    
    start = time.time()
    
    E, N, G = read_MIS(filename)
    neighb = neighbours(G,N)
    vertex = sort_vertex_by_degree(G,N)
    mis = []
    while len(vertex)!=0:
        v=vertex[0]
        vertex.remove(v)
        mis.append(v)
        for i in neighb[v-1]:
            try:
                vertex.remove(i)
            except:
                continue
    
    end = time.time()
    
    list_mis = [1 if i+1 in mis else 0 for i in range(N)]
    
    return list_mis