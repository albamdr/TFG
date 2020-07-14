
import pandas as pd
import random, numpy


from read_MVC_files import read_MVC

def greedy_mvc(E, N, G):
    
    """
    Genera un individuo para el algoritmo genético a partir de la solución del algoritmo voraz
    
    input:
        E:: Int, número de aristas
        V:: Int, número de vértiices
        G:: List, grafo en forma de lista de aristas G[i] es la lista de aristas que salen de i
    
    output:
        individual:: List, representante de la solución del algoritmo voraz
    """
    
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
        
    return individual