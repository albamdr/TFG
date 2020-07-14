import pandas as pd
import random, numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import time

from elitism import eaSimpleWithElitism
from read_MSC_files import read_MSC
from algoritmo_voraz_individuo import greedy_msc_individual

def msc(greedy, elitism, n_pop, n_gen, mat_prob, mut_prob, tournsize, nreps, filename, out1, out_filename):
    
    """
    Algoritmo genético para min set covering
    
    input:
        greedy:: Bool, indica si se añade un individuo representante de la solución obtenida por el algoritmo voraz
        elitism:: Bool, inidica si se aplica elitismo
        n_pop:: Int, tamaño de la población
        n_gen:: Int, número de generaciones
        mat_prob:: Float, probabilidad de cruce, entre 0 y 1
        mut_prob:: Float, probabilidad de mutación, entre 0 y 1
        tournsize:: Int, tamaño de torneo
        nreps:: Int, número de ejecuciones
        filename:: Str, nombre del fichero en el que se encuentra la instancia
        out1:: Str, path a la carpeta para guardar los resultados
        out_filename:: Str, nombre del fichero de salida en el que se guardan los resultados
    """

    start = time.time()
    n_rows, n_cols, rows_set, cols_set, costs_list, a, b, w = read_MSC(filename)
    #a[j] es el conjunto de columnas que cubren la fila j+1
    #b[j] es el conjunto de filas cubiertas por la columna j+1
    #w[j] es el numero de columnas que cubren la fila j+1


    creator.create("Fitness", base.Fitness, weights=(-1.0,)) #quiero minimimzar el número de conjuntos
                                                            

    #representamos los individuos en una lista
    creator.create("Individual", list, fitness=creator.Fitness)

    
    toolbox = base.Toolbox()
    toolbox.register("greedy_msc_individual", greedy_msc_individual, filename)
    toolbox.register("attr_item", random.randint, 0, 1) 
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
        toolbox.attr_item, n_cols) 
    #un individuo es una lista de 0, 1 donde individuo[i]=0 si la columna j NO forma parte del MSC
                                            #individuo[i]=1 si la columna j SÍ forma parte del MSC
    toolbox.register("individual2", tools.initIterate, creator.Individual, toolbox.greedy_msc_individual)
    toolbox.register("population", tools.initRepeat, list)


    def evalMSC(individual): 
        
        uncovered_rows = {i  for i in range(n_rows)}
        unused_cols = []
        vertex = set()
        for i in range(n_cols):
            if individual[i]==1:
                for row in b[i]:
                    uncovered_rows.discard(row-1)
            if individual[i]==0:
                unused_cols.append(i)
        
        covered = [] #lista de tuplas (columna, n de filas descubiertas que cubre columna)
        for col in unused_cols:
            n_covered = 0 #número de filas descubiertas por el individuo que recubre col
            for row in uncovered_rows:
                if row in b[col]:
                    n_covered += 1
            covered.append((col, n_covered))
        
        covered.sort(reverse=True, key=lambda x: x[1]) #ordenamos la lista por número de filas descubiertas que cubre
                                                           #la columna col de mayor a menor
        while len(uncovered_rows) != 0:
            for tup in covered:
                col, n_covered = tup
                individual[col] = 1
                for row in b[col]:
                    uncovered_rows.discard(row-1)
        
        v = sum(individual)
                
        return v,

    #mutation operator could randomly remove one vertex to the list changing a one to a zero
    def mut(individual):
        i =  random.randint(0,len(individual)-1)
        individual[i] = 0
        return individual,


    dict_result = dict()
    dict_time = dict()
    dict_all_gen = dict()
    for i in range(nreps):
        
        #register these operators in the toolbox
        toolbox.register("evaluate", evalMSC)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mut)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        
        if greedy:
            pop1 = toolbox.population(toolbox.individual, n=n_pop)
            pop2 = toolbox.population(toolbox.individual2, n=1)
            pop = pop1 + pop2
        else:
            pop = toolbox.population(toolbox.individual, n=n_pop)
        
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        if elitism:
            pop, logbook = eaSimpleWithElitism(pop, toolbox, mat_prob, mut_prob, n_gen, stats,
                                  halloffame=hof)
        else:
            pop, logbook = algorithms.eaSimple(pop, toolbox, mat_prob, mut_prob, n_gen, stats=stats, 
                            halloffame=hof)
            
        result_list = logbook
        end = time.time()
        dict_all_gen[i] = list(result_list)
        dict_result[i] = result_list[-1]
        dict_time[i] = {'time': end-start}

    dfa = pd.DataFrame.from_dict(dict_all_gen, orient = 'index')
    dfa.to_csv(out1 + out_filename + 'all_gen.csv', sep=';', header=True, index=True)
    df1 = pd.DataFrame.from_dict(dict_result, orient = 'index')
    df2 = pd.DataFrame.from_dict(dict_time, orient = 'index')
    df = pd.concat([df1,df2], axis=1, sort=False)
    df.to_csv(out1 + out_filename + 'complete.csv', sep=';', header=True, index=True)
    df = df.describe()
    df.to_csv(out1 + out_filename + '.csv', sep=';', header=True, index=True)