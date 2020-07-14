def reversed_tuples(list_of_tuples):
    
    """
    Invierte las tuplas de una lista
    
    input:
        list_of_tuples:: List, lista de tuplas
        
    output:
        l:: List, lista con las tuplas invertidas
    """
    
    l = list(reversed(list_of_tuples))
    for i in range(len(l)):
        i1, i2 = l[i]
        l[i] = (i2,i1)
    return l

def two_OPT(d, N):
    
    """
    Algoritmo 2-opt para resolver instancias del tsp
    
    input:
        d:: Array, matriz cuadrada de distancias
        N:: Int, número de filas de la matriz de distancias
        
    output:
        result:: List, lista de vértices en el orden en que se recorren
        total:: Int o Float (dependiendo de la instancia), distancia total del tour
        end-start:: Float, tiempo que tarda el algoritmo voraz en llegar a la solución, expresado en segundos
    """

    # 1. construct some Hamiltonian tour T (this can be done, for example, by the nearest-neighbor heuristic);

        # nearest neighbor algorithm
        # These are the steps of the algorithm:
        #
        #   1. Make two sets of nodes, set A and set B, and put all nodes into set B
        #   2. Put your starting node into set A
        #   3. Pick the node which is closest to the last node which was placed in set A and is not in set A; 
        #      put this closest neighbouring node into set A
        #   4. Repeat step 3 until all nodes are in set A and B is empty. 
     
    # 2. Go through every pair of edges (u,v) (u',v') and if the distance between (u,u') (v,v') is less than 
    # the current distance then swap the edeges
    
    start = time.time()

    A = [0]
    B = [i for i in range(1, N)]
    T = []
    total = 0

    for i in range(N-1):
        last = A[-1]
        ind = B[0]
        min = d[last][ind]
        for j in B[1:]: 
            new = d[last][j] 
            if min < 0 or (new > 0 and new < min): 
                min = new
                ind = j
        total += min
        A.append(ind)
        B.remove(ind)
        T.append((last,ind))
    
    fst_node = T[0][0]
    last_node = T[-1][1]
    T.append((last_node, fst_node))
    

    for i in range(len(T)-1):
        v1, w1 = T[i]

        for j in range(i+1,len(T)):
            v2, w2 = T[j]
        
            if v1 != v2 and w1 != w2:
                d1 = d[v1][w1] + d[v2][w2]
                d2 = d[v1][v2] + d[w1][w2]

                if d1 > d2 and ((v1, v2) not in T) and ((v2, v1) not in T) and ((w2, w1) not in T) and ((w1, w2) not in T):
                    new_T = T[:i]
                    new_T.append((v1,v2))
                    new_T+=(reversed_tuples(T[i+1:j]))
                    new_T.append((w1,w2))
                    new_T+=(T[j+1:])
                    
                    w1 = v2
                    T = new_T
                    
                    break
     
    total = 0
    for i in T:
        total += d[i[0]][i[1]]
        
    individual = map(lambda x: x[0], T)
    result = list(individual)

    
    end = time.time()
    
    return result, total, end-start