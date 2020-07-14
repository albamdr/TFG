
import random, numpy
import time


from read_MSC_files import read_MSC

def greedy_msc(filename):
    
    """
    Algoritmo voraz para resolver instancias de min set covering
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        msc:: List, lista de 0 y 1 donde msc[i]=1 indica que el conjunto i forma parte de la cobertura
        result:: Int, tamaño de la cobertura
        end-start:: Float, tiempo que tarda el algoritmo voraz en llegar a la solución, expresado en segundos
    """
        
    start = time.time()
    n_rows, n_cols, rows_set, cols_set, costs_list, a, b, w = read_MSC(filename)

    uncovered_rows = {i for i in range(n_rows)}
    unused_cols = {i for i in range(n_cols)}
    msc = [0 for i in range(n_cols)]

    while len(uncovered_rows) != 0:
        covered = []
        for col in unused_cols:
            n_covered = 0
            for row in uncovered_rows:
                if row in b[col]:
                    n_covered += 1
            covered.append((col, n_covered))

        covered.sort(reverse=True, key=lambda x: x[1])

        if len(covered) != 0:
            col, n_covered = covered[0]
            msc[col] = 1
            unused_cols.discard(col)
            for row in b[col]:
                uncovered_rows.discard(row - 1)
            covered.remove((col, n_covered))

    end = time.time()
    result = sum(msc)
    
    return msc, result, end-start