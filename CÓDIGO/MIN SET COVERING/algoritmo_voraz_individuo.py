import pandas as pd
import random, numpy
import time

from read_MSC_files import read_MSC

def greedy_msc_individual(filename):
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

    return msc
