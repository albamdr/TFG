
import time
import random, numpy


from read_MVC_files import read_MVC

def greedy_mvc(E, N, G):
    
    """
    Algoritmo voraz para resolver instancias de min vertex cover
    
    input:
        E:: Int, número de aristas
        N:: Int, número de vértices
        G:: List, grafo en forma de lista de aristas G[i] es la lista de aristas que salen de i
    
    output:
        mvc:: Set, conjunto de vértices pertenecientes a la cobertura
        result:: Int, tamaño de la cobertura
        end-start:: Float, tiempo que tarda el algoritmo voraz en llegar a la solución, expresado en segundos
    """
    start = time.time()
    
    mvc = set()
    edges = [edge for edges_list in G for edge in edges_list]
    tmp = [edge for edges_list in G for edge in edges_list]
    while len(edges) != 0:
        i, j = edges[0]
        mvc.add(i) #elegimos el primer vertice de la arista y lo añadimos al vertex cover

        for edge in tmp:
            if i in edge: #eliminamos todas las aristas que contengan a i
                edges.remove(edge)
            elif edge[0] > i:
                break
            tmp = edges.copy()
     
    individual=[0 for _ in range(N)]
    for i in mvc:
        individual[i-1]=1
        
    result = sum(individual)
    
    end = time.time()
    
    return mvc, result, end-start
