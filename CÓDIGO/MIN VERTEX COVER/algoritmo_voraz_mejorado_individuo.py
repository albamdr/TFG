

import pandas as pd
import random, numpy


from read_MVC_files import read_MVC

def sort_vertex_by_degree(G, N): #G=graph N=number of vertex
    
    """
    Ordena los vértices por grado, de menor a mayor
    
    input:
        G:: List, grafo en forma de lista de aristas
        N:: Int, número de vértices
        
    output:
        grades:: List, lista de vértices ordenados por grado, de mayor a menor
    """
    
    grades = [0 for i in range(N)] #lista de grados grades[i] es el grado del vértice i

    for edge in G:
        i,j = edge
        grades[i-1] +=1
        grades[j-1] +=1
    grades = [(i+1,grades[i]) for i in range(N)] #lista de la forma (vertice,grado)
    grades.sort(reverse=True, key=lambda x: x[1]) #ordenamos la lista por grado de MAYOR A MENOR
    grades = [i[0] for i in grades] #nos quedamos con los vértices ordenados
    return grades 

def greedy_mvc_mejorado(E, N, G):
    
    """
    Genera un individuo para el algoritmo genético a partir de la solución del algoritmo voraz mejorado
    
    input:
        E:: Int, número de aristas
        N:: Int, número de vértices
        G:: List, grafo en forma de lista de aristas G[i] es la lista de aristas que salen de i
    
    output:
        individual:: List, representante de la solución del algoritmo voraz mejorado
    """
    
    mvc = set()
    edges = [edge for edges_list in G for edge in edges_list]
    tmp = [edge for edges_list in G for edge in edges_list]
    while len(edges) != 0:
        vertex_sorted = sort_vertex_by_degree(edges, N)
        i = vertex_sorted[0] #vertice de mayor grado
        mvc.add(i)

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
