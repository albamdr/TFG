import numpy as np


def greedy_tsp_individual(d, N):

    """
    Genera un individuo para el algoritmo genético a partir de la solución del algoritmo voraz
    
    input:
        d:: Array, matriz cuadrada de distancias
        N:: Int, número de filas de la matriz de distancias
    
    output:
        individual:: List, representante de la solución del algoritmo voraz
    """
    

    # genera un individuo a partir de la solución del algoritmo voraz:

    # The Greedy heuristic gradually constructs a tour by repeatedly selecting the shortest edge
    # and adding it to the tour as long as it doesn’t create a cycle with less than N edges,
    # or increases the degree of any node to more than 2. We must not add the same edge twice of course.
    # Greedy, O(n2log2(n))
    #  1. Sort all edges.
    #  2. Select the shortest edge and add it to our tour if it doesn’t violate any of the above constraints.
    #  3. Dowehave N edgesinourtour? Ifno, repeat step 2.

    srted = []
    total = 0

    for i in range(N):
        for j in range(i + 1, N):
            dist = d[i][j]
            d2 = d[j][i]
            if dist < d2:
                srted.append(((i, j), dist))  # assign the edge to each distance
            else:
                srted.append(((j, i), d2))

    for i in range(N):
        srted.sort(key=lambda x: x[1])  # sorting the list by distances

    edges_sorted = map(lambda x: x[0], srted)  #
    l = list(edges_sorted)

    conexas = [[i] for i in range(N)]
    T = []
    used = [0 for i in range(N)]


    while len(conexas) != 1:

        fst = l[0]

        if used[fst[0]] < 2 and used[fst[1]] < 2:

            for c in conexas:
                if fst[0] in c:
                    c0 = c

                if fst[1] in c:
                    c1 = c

            if c0 != c1:
                conexas.append(c0 + c1)
                conexas.remove(c0)
                conexas.remove(c1)
                used[fst[0]] += 1
                used[fst[1]] += 1
                T.append(fst)
                total += d[fst[0]][fst[1]]
            l.remove(fst)

        else:
            l.remove(fst)

    last = []
    for i in range(N):
        if used[i] == 1:
            last.append(i)
    T.append((last[0], last[1]))
    total += d[last[0]][last[1]]

    sorted_T = [T[0]]
    first = T[0][1]
    T.remove(T[0])

    while len(T) > 0:
        for edge in T:
            
            if edge[0] == first:
                first = edge[1]
                sorted_T.append(edge
                T.remove(edge)
                
            elif edge[1] == first:
                sorted_T.append((edge[1], edge[0]))
                first = edge[0
                T.remove(edge)


    individual = map(lambda x: x[0], sorted_T)

    return individual
