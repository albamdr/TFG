import math

def read_MSC(filename):
    
    """
    Lee el fichero filename y devuleve la información extraída del fichero
    
    input:
        filename:: Str, nombre del fichero en el que se encuentra la instancia
    
    output:
        n_rows:: Int, número de filas
        n_cols:: Int, número de columnas
        rows_set:: Set, conjunto de todas las filas
        cols_set:: Set, conjunto de todas las columnas
        c:: List, lista de enteros c[j] es el coste de la columna j+1
        a:: List, lista de conjuntos, a[j] es el conjunto de columnas que cubren la fila j+1
        b:: List, lista de conjuntos, b[j] es el conjunto de filas cubiertas por la columna j+1
        w:: List, lista de enteros, w[j] es el numero de columnas que cubren la fila j+1
    """
        
    # Open input file
    infile = open(filename, 'r')

    # Read instance header
    num_rows, num_columns = infile.readline().strip().split()  # V: number of vertex, E: number of edges
    n_rows = int(num_rows)
    n_cols = int(num_columns)

    rows_set = {i for i in range(1,n_rows+1)} #conjunto de todas las filas
    cols_set = {i for i in range(1,n_cols+1)} #conjunto de todas las columnas

    c = [] #c[j] es el coste de la columna j+1
    for k in range(math.ceil(n_cols/12)):
        row = infile.readline().strip().split()
        for s in row:
            c.append(int(s))

    a = [set() for i in range(n_rows)] #a[j] es el conjunto de columnas que cubren la fila j+1
    b = [set() for i in range(n_cols)] #b[j] es el conjunto de filas cubiertas por la columna j+1
    w = [] #w[j] es el numero de columnas que cubren la fila j+1

    for i in range(n_rows):
        n_col = int(infile.readline())
        w.append(n_col)
        for k in range(math.ceil(n_col/12)):
            cols = infile.readline().strip().split()
            for col in cols:
                a[i].add(int(col))
                b[int(col)-1].add(i+1)

    return n_rows, n_cols, rows_set, cols_set, c, a, b, w